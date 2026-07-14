from app.collectors.github_collector import collector
from app.normalizers.github_normalizer import normalizer


class GitHubConnector:

    def collect(self, cves):

        raw = collector.collect(cves)

        normalized = {}

        for cve, advisories in raw.items():

            normalized[cve] = normalizer.normalize(advisories)

        return normalized


github_connector = GitHubConnector()
