import time

from app.jobs.job_manager import job_manager
from app.normalizers.nvd_normalizer import normalizer
from app.enrichers.enrichment_engine import engine
from app.repositories.threat_repository import threat_repository
from app.collectors.github_collector import collector as github_collector
from app.normalizers.github_normalizer import normalizer as github_normalizer
from app.merger.threat_merger import merger

class ThreatService:

    def get_all(self):
        return threat_repository.get_all()

    def sync(self):

        total_start = time.perf_counter()

        print("=" * 70)
        print("Threat Synchronization Started")
        print("=" * 70)

        #
        # Collector
        #

        start = time.perf_counter()

        job = job_manager.run("nvd")

        print(f"Job Manager          : {time.perf_counter() - start:.2f} sec")

        raw = job["raw"]

        #
        # Normalize
        #

        start = time.perf_counter()

        findings = normalizer.normalize(raw)

        cves = [finding["cve"] for finding in findings]

        github_data = github_collector.collect(cves)

        print(f"GitHub Collection        : {time.perf_counter() - start:.2f} sec")

        stored = 0

        #
        # Enrich + Store
        #

        enrich_time = 0
        mongo_time = 0
        merge_time = 0

        for nvd_finding in findings:
            t = time.perf_counter()

            github = github_data.get(nvd_finding["cve"])

            github_normalized = None

            if github:
                github_normalized = github_normalizer.normalize(github)

            threat = merger.merge(
            nvd=nvd_finding,
            github=github_normalized,
            cisa=None,
            epss=None
        )
            merge_time += time.perf_counter() - t

            enriched = engine.enrich(threat)

            enrich_time += time.perf_counter() - t

            t = time.perf_counter()

            threat_repository.upsert(enriched)

            mongo_time += time.perf_counter() - t

            stored += 1

        print(f"Enrichment           : {enrich_time:.2f} sec")
        print(f"MongoDB Upserts      : {mongo_time:.2f} sec")
        print(f"Threat Merge         : {merge_time:.2f} sec")
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
