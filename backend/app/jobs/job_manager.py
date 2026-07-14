from datetime import datetime
import time

from app.jobs.collector_registry import collector_registry


class JobManager:

    def run(self, collector_name):

        collector = collector_registry.get(collector_name)

        start_time = datetime.utcnow()

        timer = time.perf_counter()

        raw = collector.collect()

        print(f"Collector Download   : {time.perf_counter() - timer:.2f} sec")

        end_time = datetime.utcnow()

        return {
            "collector": collector_name,
            "started": start_time,
            "finished": end_time,
            "records": len(raw.get("vulnerabilities", [])),
            "status": "SUCCESS",
            "raw": raw,
        }


job_manager = JobManager()