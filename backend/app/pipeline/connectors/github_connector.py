from app.collectors.github_collector import collector
from app.normalizers.github_normalizer import normalizer
from app.utils.retry import retry


class GitHubConnector:

    def collect(self, cves):

        def fetch():
            return collector.collect(cves)

        raw = retry(fetch)
        if raw is None:
            return {}
        normalized = {}

        for cve, advisories in raw.items():

            normalized[cve] = normalizer.normalize(advisories)

        return normalized


github_connector = GitHubConnector()
