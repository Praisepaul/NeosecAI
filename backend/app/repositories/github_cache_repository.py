from pymongo import UpdateOne

from app.core.database import db
from app.core.logger import logger

from datetime import datetime, timedelta, timezone

class GitHubCacheRepository:

    COLLECTION = "github_lookup_cache"
    BATCH_SIZE = 100

    def get_recently_checked(self, cves: list[str], ttl_hours: int) -> dict:

        if not cves:
            return {}

        cutoff = datetime.now(timezone.utc) - timedelta(hours=ttl_hours)

        docs = db[self.COLLECTION].find(
            {
                "cve": {"$in": cves},
                "checked_at": {"$gte": cutoff},
            }
        )

        return {doc["cve"]: doc.get("data") for doc in docs}

    def save_many(self, items: dict):

        if not items:
            return

        operations = [
            UpdateOne(
                {"cve": cve},
                {
                    "$set": {
                        "cve": cve,
                        "data": data,
                        "checked_at": datetime.now(timezone.utc),
                    }
                },
                upsert=True,
            )
            for cve, data in items.items()
        ]

        total = len(operations)

        logger.info(
            f"[GitHub Cache] Saving {total} records " f"in batches of {self.BATCH_SIZE}"
        )

        saved = 0

        for start in range(0, total, self.BATCH_SIZE):

            batch = operations[start : start + self.BATCH_SIZE]

            try:

                result = db[self.COLLECTION].bulk_write(
                    batch,
                    ordered=False,
                )

                saved += len(batch)

                logger.info(
                    f"[GitHub Cache] Saved " f"{min(start + len(batch), total)}/{total}"
                )

                return result

            except Exception as exc:

                logger.exception(
                    f"[GitHub Cache] Batch failed "
                    f"{start}-{start + len(batch)}: {exc}"
                )

                # Do not necessarily kill the entire threat sync
                continue

        logger.info(
            f"[GitHub Cache] Completed: "
            f"{saved}/{total} batches successfully processed"
        )

github_cache_repository = GitHubCacheRepository()