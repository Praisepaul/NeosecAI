import time
from datetime import datetime, timezone
from app.jobs.collector_registry import collector_registry
from app.repositories.sync_state_repository import sync_state_repository
from app.core.logger import logger


class JobManager:

    def run(self, collector_name):

        collector = collector_registry.get(collector_name)

        start_time = datetime.now(timezone.utc)

        timer = time.perf_counter()

        if collector_name == "nvd":
            # Pull only what changed since the last successful sync,
            # instead of a fixed multi-day window every time.
            since = sync_state_repository.get_last_synced(collector_name)
            raw = collector.collect(since=since)
        else:
            raw = collector.collect()

        logger.info(
            f"[{collector_name.upper()}] Collector download took "
            f"{time.perf_counter() - timer:.2f} sec"
        )

        end_time = datetime.now(timezone.utc)

        sync_state_repository.set_last_synced(collector_name, end_time)

        return {
            "collector": collector_name,
            "started": start_time,
            "finished": end_time,
            "records": len(raw.get("vulnerabilities", [])),
            "status": "SUCCESS",
            "raw": raw,
        }


job_manager = JobManager()