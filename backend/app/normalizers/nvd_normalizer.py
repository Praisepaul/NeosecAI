from copy import deepcopy

from app.normalizers.base_normalizer import BaseNormalizer


class NVDNormalizer(BaseNormalizer):

    REJECTED_MARKERS = (
        "rejected or withdrawn",
        "this cve id has been rejected",
        "this cve has been rejected",
        "rejected reason:",
    )

    # ==========================================================
    # CVSS
    # ==========================================================

    def extract_cvss(self, cve):

        metrics = cve.get("metrics") or {}

        versions = [
            "cvssMetricV40",
            "cvssMetricV31",
            "cvssMetricV30",
            "cvssMetricV2",
        ]

        for version in versions:

            metric_list = metrics.get(version)

            if not metric_list:
                continue

            metric = metric_list[0] or {}

            data = metric.get("cvssData") or {}

            return {
                "version": version.replace("cvssMetric", ""),
                "severity": (
                    data.get("baseSeverity")
                    or metric.get("baseSeverity")
                    or "UNKNOWN"
                ),
                "score": data.get("baseScore"),
                "vector": data.get("vectorString"),
            }

        return {
            "version": None,
            "severity": "UNKNOWN",
            "score": None,
            "vector": None,
        }

    # ==========================================================
    # DESCRIPTION
    # ==========================================================

    def extract_description(self, cve):

        descriptions = cve.get("descriptions") or []

        for description in descriptions:

            if (
                isinstance(description, dict)
                and description.get("lang") == "en"
            ):

                value = description.get("value")

                if isinstance(value, str):

                    return value.strip()

        return None

    # ==========================================================
    # REJECTED / WITHDRAWN CVE DETECTION
    # ==========================================================

    def is_rejected(self, cve):

        description = self.extract_description(cve)

        if not description:

            return False

        normalized = description.lower().strip()

        return any(
            marker in normalized
            for marker in self.REJECTED_MARKERS
        )

    # ==========================================================
    # TECHNOLOGY EXTRACTION
    # ==========================================================

    def extract_technology(self, cve):

        vendors = set()
        products = set()
        packages = set()
        repositories = set()
        versions = set()

        #
        # Legacy affected structure
        #

        for affected in cve.get("affected", []) or []:

            if not isinstance(affected, dict):
                continue

            for item in affected.get("affectedData", []) or []:

                if not isinstance(item, dict):
                    continue

                vendor = item.get("vendor")
                product = item.get("product")
                package = item.get("packageName")
                repository = item.get("repo")

                if vendor:
                    vendors.add(str(vendor).strip().lower())

                if product:
                    products.add(str(product).strip().lower())

                if package:
                    packages.add(str(package).strip().lower())

                if repository:
                    repositories.add(str(repository).strip())

                for version in item.get("versions", []) or []:

                    if not isinstance(version, dict):
                        continue

                    version_text = version.get("version")

                    if not version_text:
                        continue

                    version_text = str(version_text)

                    if version.get("lessThan"):

                        version_text += (
                            f" < {version['lessThan']}"
                        )

                    elif version.get("lessThanOrEqual"):

                        version_text += (
                            f" <= {version['lessThanOrEqual']}"
                        )

                    versions.add(version_text)

        #
        # Modern NVD CPE configuration structure
        #

        for configuration in cve.get("configurations", []) or []:

            if not isinstance(configuration, dict):
                continue

            for node in configuration.get("nodes", []) or []:

                if not isinstance(node, dict):
                    continue

                for match in node.get("cpeMatch", []) or []:

                    if not isinstance(match, dict):
                        continue

                    criteria = match.get("criteria")

                    if not criteria:
                        continue

                    parts = criteria.split(":")

                    # cpe:2.3:a:vendor:product:version...
                    if (
                        len(parts) >= 5
                        and parts[0] == "cpe"
                        and parts[1] == "2.3"
                    ):

                        vendor = parts[3]
                        product = parts[4]
                        version = parts[5] if len(parts) > 5 else None

                        if vendor and vendor != "*":
                            vendors.add(vendor.lower())

                        if product and product != "*":
                            products.add(product.lower())

                        if version and version != "*":
                            versions.add(version)

        return {
            "vendors": sorted(vendors),
            "products": sorted(products),
            "packages": sorted(packages),
            "repositories": sorted(repositories),
            "ecosystems": [],
            "versions": sorted(versions),
        }

    # ==========================================================
    # CWE EXTRACTION
    # ==========================================================

    def extract_cwes(self, cve):

        cwes = set()

        for weakness in cve.get("weaknesses", []) or []:

            if not isinstance(weakness, dict):
                continue

            for description in weakness.get("description", []) or []:

                if not isinstance(description, dict):
                    continue

                value = description.get("value")

                if value:
                    cwes.add(value)

        return sorted(cwes)

    # ==========================================================
    # NORMALIZATION
    # ==========================================================

    def normalize(self, raw):

        findings = []

        vulnerabilities = raw.get("vulnerabilities", []) or []

        for item in vulnerabilities:

            if not isinstance(item, dict):
                continue

            cve = item.get("cve") or {}

            cve_id = cve.get("id")

            if not cve_id:
                continue

            #
            # Do not store rejected/withdrawn CVEs
            #

            if self.is_rejected(cve):

                print(
                    f"[NVD] Skipping rejected/withdrawn CVE: {cve_id}"
                )

                continue

            description = self.extract_description(cve)

            finding = {
                # Canonical identity
                "cve": cve_id,
                "title": description,
                "description": description,
                "published": cve.get("published"),
                "modified": cve.get("lastModified"),
                "cvss": self.extract_cvss(cve),
                "technology": self.extract_technology(cve),
                "cwes": self.extract_cwes(cve),
                "references": [
                    reference.get("url")
                    for reference in cve.get("references", []) or []
                    if isinstance(reference, dict) and reference.get("url")
                ],
                # Source-specific information
                "source": ["NVD"],
                # Preserve the complete original NVD CVE object
                "raw": deepcopy(cve),
            }

            findings.append(finding)

        return findings


normalizer = NVDNormalizer()
