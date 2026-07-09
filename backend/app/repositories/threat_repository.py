from app.core.database import db
from app.repositories.base_repository import BaseRepository


class ThreatRepository(BaseRepository):

    def __init__(self):
        super().__init__(db.threats)


threat_repository = ThreatRepository()