import time
from datetime import datetime, timedelta, timezone

import httpx

from app.config.settings import settings
from app.core.logger import logger

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Small safety overlap so a CVE modified right at the edge of the
# previous sync window is never missed due to clock drift / latency.
OVERLAP_MINUTES = 30


class NVDCollector:

    def collect(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
    ):

        end = datetime.now(timezone.utc)

        if since:
            start = since - timedelta(minutes=OVERLAP_MINUTES)
            logger.info(f"[NVD] Incremental sync since {start.isoformat()}")
        else:
            start = end - timedelta(days=settings.nvd_sync_days)
            logger.info(
                f"[NVD] No previous sync recorded - using "
                f"{settings.nvd_sync_days}-day fallback window"
            )

        start_date = start.isoformat(timespec="seconds").replace("+00:00", "Z")
        end_date = end.isoformat(timespec="seconds").replace("+00:00", "Z")

        page_size = settings.nvd_results_per_page
        start_index = 0

        all_vulnerabilities = []
        total_results = None

        headers = {"apiKey": settings.nvd_api_key} if settings.nvd_api_key else {}

        # Without a key: 5 requests/30s -> 6s between pages.
        # With a key:   50 requests/30s -> 0.6s is a safe margin.
        page_delay = 0.6 if settings.nvd_api_key else 6

        with httpx.Client(timeout=settings.http_timeout, headers=headers) as client:

            while True:

                params = {
                    "lastModStartDate": start_date,
                    "lastModEndDate": end_date,
                    "resultsPerPage": page_size,
                    "startIndex": start_index,
                }

                response = client.get(NVD_URL, params=params)

                response.raise_for_status()

                data = response.json()

                if total_results is None:
                    total_results = data.get("totalResults", 0)

                vulnerabilities = data.get("vulnerabilities", [])

                # No results means there is nothing more to download
                if not vulnerabilities:
                    logger.info("[NVD] No more vulnerabilities returned")
                    break

                all_vulnerabilities.extend(vulnerabilities)

                logger.info(
                    "[NVD] Page: startIndex=%s | received=%s | total=%s",
                    start_index,
                    len(vulnerabilities),
                    total_results,
                )

                # If the API returned fewer records than requested,
                # this is the final page.
                if len(vulnerabilities) < page_size:
                    break

                start_index += len(vulnerabilities)

                if start_index >= total_results:
                    break

                # Prevent NVD rate limiting
                time.sleep(page_delay)

        return {
            "resultsPerPage": len(all_vulnerabilities),
            "startIndex": 0,
            "totalResults": len(all_vulnerabilities),
            "vulnerabilities": all_vulnerabilities,
        }


collector = NVDCollector()


from app.jobs.collector_registry import collector_registry

collector_registry.register("nvd", collector)
