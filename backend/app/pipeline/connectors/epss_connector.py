import requests

from app.config.settings import settings
from app.utils.retry import retry


class EPSSConnector:

    BASE_URL = "https://api.first.org/data/v1/epss"

    def collect(self, cves):

        if not cves:
            return {}

        findings = {}

        batch_size = 100

        for i in range(0, len(cves), batch_size):

            batch = cves[i : i + batch_size]

            def fetch():

                response = requests.get(
                    self.BASE_URL,
                    params={"cve": ",".join(batch)},
                    timeout=settings.http_timeout,
                )

                response.raise_for_status()

                return response

            try:

                response = retry(fetch)

                if response is None:
                    continue

                data = response.json().get("data", [])

                for item in data:

                    findings[item["cve"]] = {
                        "score": float(item["epss"]),
                        "percentile": float(item["percentile"]),
                    }

                print(
                    f"[EPSS] Processed "
                    f"{min(i + batch_size, len(cves))}"
                    f"/{len(cves)} CVEs"
                )

            except Exception as ex:

                print(f"[EPSS] Batch failed: {ex}")

        print(f"[EPSS] Successfully collected " f"{len(findings)} scores")

        return findings


epss_connector = EPSSConnector()
