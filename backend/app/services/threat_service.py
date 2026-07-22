import time

from app.pipeline.threat_pipeline import pipeline
from app.enrichers.enrichment_engine import engine
from app.repositories.threat_repository import threat_repository
from app.repositories.sync_state_repository import sync_state_repository

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

        logger.info(f"Collector Download       : " f"{timings['collector']:.2f} sec")

        logger.info(
            f"NVD Normalize            : " f"{timings['nvd_normalization']:.2f} sec"
        )

        logger.info(
            f"Intelligence Collection  : "
            f"{timings['intelligence_collection']:.2f} sec"
        )

        logger.info(f"Threat Merge             : " f"{timings['merge']:.2f} sec")

        # =========================================================
        # ENRICHMENT
        # =========================================================

        assets = asset_repository.get_all()

        enrich_start = time.perf_counter()

        enriched_threats = [
            engine.enrich(
                asset_matcher.match(
                    threat,
                    assets=assets,
                )
            )
            for threat in threats
        ]

        enrich_time = time.perf_counter() - enrich_start

        # =========================================================
        # DATABASE WRITE
        # =========================================================

        mongo_start = time.perf_counter()

        write_result = threat_repository.bulk_upsert(
            enriched_threats
        )

        mongo_time = time.perf_counter() - mongo_start

        logger.info(
            f"Enrichment                : {enrich_time:.2f} sec"
        )

        logger.info(
            f"MongoDB Bulk Write         : {mongo_time:.2f} sec"
        )

        # Only now is the NVD batch considered successfully processed
        sync_state_repository.set_last_synced(
            "nvd",
            job["finished"],
        )

        logger.info(
            "[SYNC] NVD sync state updated after successful threat persistence"
        )

        # =========================================================
        # COMMIT SYNC STATE ONLY AFTER SUCCESSFUL DATABASE WRITE
        # =========================================================

        sync_state_repository.set_last_synced(
            collector_name="nvd",
            when=job["finished"],
        )

        logger.info(
            f"[SYNC] NVD sync state updated to " f"{job['finished'].isoformat()}"
        )

        logger.info(f"Enrichment                : " f"{enrich_time:.2f} sec")

        logger.info(f"MongoDB Bulk Write        : " f"{mongo_time:.2f} sec")

        logger.info("-" * 70)

        logger.info(
            f"TOTAL                     : "
            f"{time.perf_counter() - total_start:.2f} sec"
        )

        logger.info("=" * 70)

        return {
            "status": "SUCCESS",
            "collector": "nvd",
            "downloaded": job["records"],
            "stored": (write_result["modified"] + write_result["upserted"]),
            "started": job["started"],
            "finished": job["finished"],
        }


threat_service = ThreatService()
