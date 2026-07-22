import time

from app.pipeline.threat_pipeline import pipeline
from app.enrichers.enrichment_engine import engine
from app.repositories.threat_repository import threat_repository
from app.assets.asset_matcher import asset_matcher
from app.assets.asset_repository import asset_repository
from app.core.logger import logger


class ThreatService:

    def get_all(self):
        return threat_repository.get_all_summaries()

    def get_by_cve(self, cve: str):
        return threat_repository.get_by_cve(cve)

    def sync(self):

        total_start = time.perf_counter()

        logger.info("=" * 70)
        logger.info("Threat Synchronization Started")
        logger.info("=" * 70)

        pipeline_result = pipeline.run()

        job = pipeline_result["job"]
        threats = pipeline_result["threats"]
        timings = pipeline_result["timings"]

        logger.info(f"Collector Download       : {timings['collector']:.2f} sec")
        logger.info(
            f"NVD Normalize             : {timings['nvd_normalization']:.2f} sec"
        )
        logger.info(
            f"Intelligence Collection   : {timings['intelligence_collection']:.2f} sec"
        )
        logger.info(f"Threat Merge              : {timings['merge']:.2f} sec")

        assets = asset_repository.get_all()

        enrich_start = time.perf_counter()

        enriched_threats = [
            engine.enrich(asset_matcher.match(threat, assets=assets))
            for threat in threats
        ]

        enrich_time = time.perf_counter() - enrich_start

        
        mongo_start = time.perf_counter()

        write_result = threat_repository.bulk_upsert(enriched_threats)

        mongo_time = time.perf_counter() - mongo_start

        logger.info(f"Enrichment                : {enrich_time:.2f} sec")
        logger.info(f"MongoDB Bulk Write         : {mongo_time:.2f} sec")

        logger.info("-" * 70)
        logger.info(
            f"TOTAL                      : {time.perf_counter() - total_start:.2f} sec"
        )
        logger.info("=" * 70)

        return {
            "status": "SUCCESS",
            "collector": "nvd",
            "downloaded": job["records"],
            "stored": write_result["modified"] + write_result["upserted"],
            "started": job["started"],
            "finished": job["finished"],
        }


threat_service = ThreatService()
