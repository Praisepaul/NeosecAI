import httpx

URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


class CISACollector:

    def collect(self):

        response = httpx.get(

            URL,

            timeout=60

        )

        response.raise_for_status()

        kev = {}

        for vuln in response.json()["vulnerabilities"]:

            kev[vuln["cveID"]] = vuln

        return kev


collector = CISACollector()

from app.jobs.collector_registry import collector_registry

collector_registry.register(
    "cisa",
    collector
)