import httpx

from app.config.settings import settings

URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


class CISACollector:

    def collect(self):

        response = httpx.get(URL, timeout=settings.http_timeout)

        response.raise_for_status()

        kev = {}

        for vuln in response.json()["vulnerabilities"]:
            kev[vuln["cveID"]] = vuln

        return kev


collector = CISACollector()
