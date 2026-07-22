from app.collectors.github_collector import collector
from app.config.settings import settings
from app.core.logger import logger
from app.repositories.github_cache_repository import github_cache_repository
from app.utils.retry import retry


class GitHubConnector:

    def collect(self, cves):

        if not cves:
            return {}

        cached = github_cache_repository.get_recently_checked(
            cves, settings.github_cache_ttl_hours
        )

        remaining = [cve for cve in cves if cve not in cached]

        logger.info(
            f"[GitHub] {len(cached)} CVEs served from cache, "
            f"{len(remaining)} require a live lookup"
        )

        fresh = {}

        if remaining:

            def fetch():
                return collector.collect(remaining)

            fresh = retry(fetch) or {}

            # Persist EVERY CVE we checked, including ones with no
            # advisory (data=None), so we don't re-ask GitHub about
            # them again inside the TTL window.
            to_cache = {cve: fresh.get(cve) for cve in remaining}
            github_cache_repository.save_many(to_cache)

        merged = {**cached, **fresh}

        return {cve: data for cve, data in merged.items() if data}


github_connector = GitHubConnector()
