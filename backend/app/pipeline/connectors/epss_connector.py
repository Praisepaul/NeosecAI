import requests
from app.config.settings import settings
from app.utils.retry import retry


class EPSSConnector:

    BASE_URL = "https://api.first.org/data/v1/epss"

    def collect(self, cves):

        if not cves:
            return {}

        def fetch():

            response = requests.get(
                self.BASE_URL,
                params={"cve": ",".join(cves)},
                timeout=settings.http_timeout,
            )

            response.raise_for_status()

            return response

        try:

            response = retry(fetch)
            
            if response is None:
                return {}
            
            data = response.json().get("data", [])

            findings = {}

            for item in data:

                findings[item["cve"]] = {
                    "score": float(item["epss"]),
                    "percentile": float(item["percentile"]),
                }

            return findings

        except Exception as ex:

            print(f"[EPSS] Failed: {ex}")

            return {}


epss_connector = EPSSConnector()
