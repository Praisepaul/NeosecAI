import time
from app.pipeline.threat_pipeline import pipeline
from app.enrichers.enrichment_engine import engine
from app.repositories.threat_repository import threat_repository
from app.assets.asset_matcher import asset_matcher

class ThreatService:

    def get_all(self):
        return threat_repository.get_all()

    def sync(self):

        total_start = time.perf_counter()

        print("=" * 70)
        print("Threat Synchronization Started")
        print("=" * 70)

        pipeline_result = pipeline.run()

        job = pipeline_result["job"]

        threats = pipeline_result["threats"]

        timings = pipeline_result["timings"]

        print(f"Collector Download : {timings['collector']:.2f} sec")
        print(f"NVD Normalize      : {timings['nvd_normalization']:.2f} sec")
        print(f"Intelligence Collection : {timings['intelligence_collection']:.2f} sec")
        print(f"Threat Merge       : {timings['merge']:.2f} sec")

        stored = 0

        #
        # Enrich + Store
        #

        enrich_time = 0
        mongo_time = 0

        for threat in threats:

            t = time.perf_counter()

            threat = asset_matcher.match(threat)

            enriched = engine.enrich(threat)

            enrich_time += time.perf_counter() - t

            t = time.perf_counter()

            threat_repository.upsert(enriched)

            mongo_time += time.perf_counter() - t

            stored += 1

        print(f"Enrichment           : {enrich_time:.2f} sec")

        print(f"MongoDB Upserts      : {mongo_time:.2f} sec")

        print("-" * 70)
        print(f"TOTAL                : {time.perf_counter() - total_start:.2f} sec")
        print("=" * 70)

        return {
            "status": "SUCCESS",
            "collector": "nvd",
            "downloaded": job["records"],
            "stored": stored,
            "started": job["started"],
            "finished": job["finished"],
        }


threat_service = ThreatService()
