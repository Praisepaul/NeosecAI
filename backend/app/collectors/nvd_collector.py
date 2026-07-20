import httpx
import time

from datetime import datetime, timedelta, timezone

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


class NVDCollector:

    def collect(self, days: int = 7):

        end = datetime.now(timezone.utc)
        start = end - timedelta(days=days)

        start_date = start.isoformat(timespec="seconds").replace("+00:00", "Z")

        end_date = end.isoformat(timespec="seconds").replace("+00:00", "Z")

        page_size = 100
        start_index = 0

        all_vulnerabilities = []
        total_results = None

        with httpx.Client(timeout=60) as client:

            while True:

                params = {
                    "pubStartDate": start_date,
                    "pubEndDate": end_date,
                    "resultsPerPage": page_size,
                    "startIndex": start_index,
                }

                response = client.get(NVD_URL, params=params)

                response.raise_for_status()

                data = response.json()

                if total_results is None:

                    total_results = data.get("totalResults", 0)

                vulnerabilities = data.get("vulnerabilities", [])

                all_vulnerabilities.extend(vulnerabilities)

                print(
                    f"[NVD] Downloaded "
                    f"{len(all_vulnerabilities)}"
                    f"/{total_results}"
                )

                if len(all_vulnerabilities) >= total_results:

                    break

                start_index += page_size

                # Prevent NVD rate limiting
                time.sleep(6)

        return {
            "resultsPerPage": len(all_vulnerabilities),
            "startIndex": 0,
            "totalResults": len(all_vulnerabilities),
            "vulnerabilities": (all_vulnerabilities),
        }


collector = NVDCollector()


from app.jobs.collector_registry import collector_registry

collector_registry.register("nvd", collector)
