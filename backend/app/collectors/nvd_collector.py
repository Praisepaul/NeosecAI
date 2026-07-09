import httpx
from datetime import datetime, timedelta, timezone

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


class NVDCollector:

    def collect(self, days: int = 7):

        end = datetime.now(timezone.utc)
        start = end - timedelta(days=days)

        params = {
            "pubStartDate": start.isoformat(timespec="seconds").replace("+00:00", "Z"),
            "pubEndDate": end.isoformat(timespec="seconds").replace("+00:00", "Z"),
            "resultsPerPage": 100
        }

        response = httpx.get(
            NVD_URL,
            params=params,
            timeout=60
        )

        response.raise_for_status()

        return response.json()


collector = NVDCollector()

from app.jobs.collector_registry import collector_registry

collector_registry.register("nvd", collector)