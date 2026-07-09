from datetime import datetime

from app.jobs.collector_registry import collector_registry


class JobManager:

    def run(self, collector_name):

        collector = collector_registry.get(collector_name)

        start = datetime.utcnow()

        raw = collector.collect()

        end = datetime.utcnow()

        return {
            "collector": collector_name,
            "started": start,
            "finished": end,
            "records": len(raw.get("vulnerabilities", [])),
            "status": "SUCCESS",
            "raw": raw,
        }


job_manager = JobManager()