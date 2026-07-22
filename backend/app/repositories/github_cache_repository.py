from datetime import datetime, timedelta, timezone

from pymongo import UpdateOne

from app.core.database import db
from app.core.logger import logger


class GitHubCacheRepository:
    """Persists GitHub advisory lookups (including "no advisory found"
    results) so repeated syncs don't re-query GitHub for the same CVE
    inside the TTL window, and so we survive process restarts."""

    COLLECTION = "github_lookup_cache"

    def get_recently_checked(self, cves: list[str], ttl_hours: int) -> dict:

        if not cves:
            return {}

        cutoff = datetime.now(timezone.utc) - timedelta(hours=ttl_hours)

        docs = db[self.COLLECTION].find(
            {"cve": {"$in": cves}, "checked_at": {"$gte": cutoff}}
        )

        return {doc["cve"]: doc.get("data") for doc in docs}

    def save_many(self, results: dict) -> None:

        if not results:
            return

        now = datetime.now(timezone.utc)

        operations = [
            UpdateOne(
                {"cve": cve},
                {"$set": {"cve": cve, "data": data, "checked_at": now}},
                upsert=True,
            )
            for cve, data in results.items()
        ]

        result = db[self.COLLECTION].bulk_write(operations, ordered=False)

        logger.info(
            f"[GitHub Cache] saved {len(operations)} lookups "
            f"(matched={result.matched_count}, upserted={len(result.upserted_ids or {})})"
        )


github_cache_repository = GitHubCacheRepository()
