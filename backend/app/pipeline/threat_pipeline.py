import time

from app.jobs.job_manager import job_manager
from app.normalizers.nvd_normalizer import normalizer as nvd_normalizer
from app.merger.threat_merger import merger
from app.pipeline.connectors.github_connector import github_connector
from app.pipeline.connectors.cisa_connector import cisa_connector
from app.pipeline.connectors.epss_connector import epss_connector

class ThreatPipeline:

    def run(self):

        timings = {}

        #
        # -------------------------------------------------------------
        # STEP 1 - Download NVD Feed
        # -------------------------------------------------------------
        #

        start = time.perf_counter()

        job = job_manager.run("nvd")

        timings["collector"] = time.perf_counter() - start

        raw = job["raw"]

        #
        # -------------------------------------------------------------
        # STEP 2 - Normalize NVD
        # -------------------------------------------------------------
        #

        start = time.perf_counter()

        nvd_findings = nvd_normalizer.normalize(raw)

        timings["nvd_normalization"] = time.perf_counter() - start

        #
        # -------------------------------------------------------------
        # STEP 3 - Collect GitHub Advisories
        # -------------------------------------------------------------
        #

        cves = [finding["cve"] for finding in nvd_findings]

        start = time.perf_counter()

        github_data = github_connector.collect(cves)        

        timings["github_collection"] = time.perf_counter() - start

        #
        # -------------------------------------------------------------
        # STEP 4 - Merge Threat Intelligence
        # -------------------------------------------------------------
        #

        merged_threats = []

        start = time.perf_counter()

        for nvd in nvd_findings:

            github = github_data.get(nvd["cve"])

            threat = merger.merge(
                nvd=nvd,
                github=github,
                cisa=None,
                epss=None
            )

            merged_threats.append(threat)

        timings["merge"] = time.perf_counter() - start

        return {"job": job, "threats": merged_threats, "timings": timings}


pipeline = ThreatPipeline()
