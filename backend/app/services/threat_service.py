from app.jobs.job_manager import job_manager
from app.normalizers.nvd_normalizer import normalizer
from app.enrichers.enrichment_engine import engine
from app.repositories.threat_repository import threat_repository


class ThreatService:

    def get_all(self):
        return threat_repository.get_all()

    def sync(self):

        # Run collector through Job Manager
        job = job_manager.run("nvd")

        raw = job["raw"]

        # Normalize
        findings = normalizer.normalize(raw)

        stored = 0

        # Enrich + Store
        for finding in findings:

            enriched = engine.enrich(finding)

            threat_repository.upsert(enriched)

            stored += 1

        return {
            "status": "SUCCESS",
            "collector": "nvd",
            "downloaded": job["records"],
            "stored": stored,
            "started": job["started"],
            "finished": job["finished"],
        }


threat_service = ThreatService()
