from app.core.database import db
from app.repositories.base_repository import BaseRepository


class ThreatRepository(BaseRepository):

    SUMMARY_PROJECTION = {
        "_id": 0,
        "cve": 1,
        "title": 1,
        "published": 1,
        "modified": 1,
        "cvss": 1,
        "epss": 1,
        "kev": 1,
        "risk_score": 1,
        "matched": 1,
        "matched_assets": 1,
        "matched_products": 1,
    }

    def __init__(self):
        super().__init__(db.threats)

    def get_all_summaries(self):
        return self.get_all(projection=self.SUMMARY_PROJECTION)

    def get_by_cve(self, cve: str):
        return self.get_by_key(
            key="cve",
            value=cve,
            projection={"_id": 0},
        )


threat_repository = ThreatRepository()
