import time

from concurrent.futures import ThreadPoolExecutor

from app.jobs.job_manager import job_manager

from app.normalizers.nvd_normalizer import normalizer as nvd_normalizer
from app.normalizers.github_normalizer import normalizer as github_normalizer
from app.normalizers.cisa_normalizer import normalizer as cisa_normalizer

from app.merger.threat_merger import merger

from app.pipeline.connectors.github_connector import github_connector
from app.pipeline.connectors.cisa_connector import cisa_connector
from app.pipeline.connectors.epss_connector import epss_connector

from app.matching.product_matcher import matcher
from app.core.logger import logger


class ThreatPipeline:

    def run(self):

        timings = {}

        
        # STEP 1 - Download NVD
        
        start = time.perf_counter()

        job = job_manager.run("nvd")

        timings["collector"] = time.perf_counter() - start

        raw = job["raw"]

        
        # STEP 2 - Normalize + filter to only what's in our
        # technology inventory (config/technology_inventory.json)
        
        start = time.perf_counter()

        nvd_findings = nvd_normalizer.normalize(raw)

        relevant_findings = []

        for finding in nvd_findings:

            products = finding.get("technology", {}).get("products", [])

            matches = matcher.match(products)

            if matches:
                finding["matched_products"] = matches
                relevant_findings.append(finding)

        logger.info(f"[FILTER] NVD CVEs: {len(nvd_findings)}")
        logger.info(f"[FILTER] Relevant CVEs: {len(relevant_findings)}")

        nvd_findings = relevant_findings

        timings["nvd_normalization"] = time.perf_counter() - start

        
        # STEP 3 - Collect external intelligence (parallel)
        
        cves = [finding["cve"] for finding in nvd_findings]

        start = time.perf_counter()

        with ThreadPoolExecutor(max_workers=3) as executor:

            github_future = executor.submit(github_connector.collect, cves)
            cisa_future = executor.submit(cisa_connector.collect, cves)
            epss_future = executor.submit(epss_connector.collect, cves)

            github_data = github_future.result() or {}
            cisa_data = cisa_future.result() or {}
            epss_data = epss_future.result() or {}

        timings["intelligence_collection"] = time.perf_counter() - start

        normalized_github = {}

        for cve, advisories in github_data.items():

            normalized = github_normalizer.normalize(advisories)

            if normalized:
                normalized_github[cve] = normalized

        normalized_cisa = {}

        for cve, vuln in cisa_data.items():

            normalized = cisa_normalizer.normalize(vuln)

            if normalized:
                normalized_cisa[cve] = normalized

        #
        # STEP 5 - Merge
        #
        merged_threats = []

        start = time.perf_counter()

        for nvd in nvd_findings:

            cve = nvd["cve"]

            threat = merger.merge(
                nvd=nvd,
                github=normalized_github.get(cve),
                cisa=normalized_cisa.get(cve),
                epss=epss_data.get(cve),
            )

            merged_threats.append(threat)

        timings["merge"] = time.perf_counter() - start

        return {
            "job": job,
            "threats": merged_threats,
            "timings": timings,
        }


pipeline = ThreatPipeline()
