from app.repositories.threat_repository import threat_repository


class ThreatService:

    def get_all(self):
        return threat_repository.get_all()


threat_service = ThreatService()