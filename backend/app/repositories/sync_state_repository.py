from datetime import datetime

from app.core.database import db


class SyncStateRepository:
    """Tracks the last successful sync timestamp per collector, so NVD
    syncs can pull only what changed since last time instead of
    re-downloading a fixed multi-day window every run."""

    COLLECTION = "sync_state"

    def get_last_synced(self, collector_name: str) -> datetime | None:

        doc = db[self.COLLECTION].find_one({"collector": collector_name})

        return doc.get("last_synced") if doc else None

    def set_last_synced(self, collector_name: str, when: datetime) -> None:

        db[self.COLLECTION].update_one(
            {"collector": collector_name},
            {"$set": {"collector": collector_name, "last_synced": when}},
            upsert=True,
        )


sync_state_repository = SyncStateRepository()
