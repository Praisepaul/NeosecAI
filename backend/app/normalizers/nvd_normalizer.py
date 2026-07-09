from app.normalizers.base_normalizer import BaseNormalizer


class NVDNormalizer(BaseNormalizer):

    def extract_cvss(self, cve):

        metrics = cve.get("metrics", {})

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

            metric = metric_list[0]

            data = metric.get("cvssData", {})

            return {
                "version": version.replace("cvssMetric", ""),
                "severity": data.get("baseSeverity")
                or metric.get("baseSeverity")
                or "UNKNOWN",
                "score": data.get("baseScore"),
                "vector": data.get("vectorString"),
            }

        return {
            "version": None,
            "severity": "UNKNOWN",
            "score": None,
            "vector": None,
        }

    def extract_technology(self, cve):

        vendors = set()
        products = set()
        packages = set()
        repositories = set()
        versions = []

        #
        # 1. affected
        #

        for affected in cve.get("affected", []):

            for item in affected.get("affectedData", []):

                vendor = item.get("vendor")
                product = item.get("product")
                package = item.get("packageName")
                repo = item.get("repo")

                if vendor:
                    vendors.add(vendor.lower())

                if product:
                    products.add(product.lower())

                if package:
                    packages.add(package.lower())

                if repo:
                    repositories.add(repo)

                for version in item.get("versions", []):

                    version_text = version.get("version", "")

                    if version.get("lessThan"):

                        version_text += f" < {version['lessThan']}"

                    elif version.get("lessThanOrEqual"):

                        version_text += f" <= {version['lessThanOrEqual']}"

                    versions.append(version_text)

        #
        # 2. configurations (CPE)
        #

        for configuration in cve.get("configurations", []):

            for node in configuration.get("nodes", []):

                for match in node.get("cpeMatch", []):

                    criteria = match.get("criteria", "")

                    parts = criteria.split(":")

                    if len(parts) > 4:

                        vendors.add(parts[3].lower())
                        products.add(parts[4].lower())

        return {

            "vendors": sorted(vendors),

            "products": sorted(products),

            "packages": sorted(packages),

            "repositories": sorted(repositories),

            "versions": versions,

        }

    def normalize(self, raw):

        findings = []

        for item in raw.get("vulnerabilities", []):

            cve = item["cve"]

            cvss = self.extract_cvss(cve)

            technology = self.extract_technology(cve)

            description = ""

            for desc in cve.get("descriptions", []):

                if desc.get("lang") == "en":

                    description = desc.get("value", "")

                    break

            finding = {

                "cve": cve.get("id"),

                "title": description[:100] if description else cve.get("id"),

                "summary": description,

                "published": cve.get("published"),

                "modified": cve.get("lastModified"),

                "cvss": cvss,

                "technology": technology,

                "matched": False,

                "matched_assets": [],

                "risk_score": 0,

                "kev": False,

                "epss": None,

                "exploit_available": False,

                "references": [
                    ref.get("url")
                    for ref in cve.get("references", [])
                    if ref.get("url")
                ],

                "source": ["NVD"],

                "last_synced": None,

            }

            findings.append(finding)

        return findings


normalizer = NVDNormalizer()