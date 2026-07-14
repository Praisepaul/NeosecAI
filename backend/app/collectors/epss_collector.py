import httpx

EPSS_URL = "https://api.first.org/data/v1/epss"


class EPSSCollector:

    def collect(self, cves):

        if not cves:
            return {}

        response = httpx.get(

            EPSS_URL,

            params={
                "cve": ",".join(cves)
            },

            timeout=60
        )

        response.raise_for_status()

        data = response.json().get("data", [])

        result = {}

        for item in data:

            result[item["cve"]] = {

                "epss": float(item["epss"]),

                "percentile": float(item["percentile"])

            }

        return result


collector = EPSSCollector()

from app.jobs.collector_registry import collector_registry

collector_registry.register(
    "epss",
    collector
)