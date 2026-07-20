from copy import deepcopy

from app.normalizers.base_normalizer import BaseNormalizer


class GitHubNormalizer(BaseNormalizer):

    def normalize(self, advisories):

        if not advisories:
            return None

        # GitHub collector currently returns one advisory as a dictionary
        if isinstance(advisories, dict):

            advisory = advisories

        # Support a list of advisories as well
        elif isinstance(advisories, list):

            if not advisories:
                return None

            advisory = advisories[0]

        else:

            return None

        if not isinstance(advisory, dict):
            return None

        #
        # CVE
        #

        cve = advisory.get("cve_id")

        if not cve:
            return None

        #
        # CVSS
        #

        cvss_data = advisory.get("cvss")

        if not isinstance(cvss_data, dict):
            cvss_data = {}

        score = cvss_data.get("score")

        vector = cvss_data.get("vector_string") or cvss_data.get("vector")

        #
        # Vulnerabilities / Packages
        #

        packages = []
        ecosystems = []
        patched_versions = []

        vulnerabilities = advisory.get("vulnerabilities") or []

        for vulnerability in vulnerabilities:

            if not isinstance(vulnerability, dict):
                continue

            package = vulnerability.get("package")

            if isinstance(package, dict):

                package_name = package.get("name")

                ecosystem = package.get("ecosystem")

                if package_name:
                    packages.append(package_name)

                if ecosystem:
                    ecosystems.append(ecosystem)

            patched = vulnerability.get("first_patched_version")

            if isinstance(patched, dict):

                identifier = patched.get("identifier")

                if identifier:
                    patched_versions.append(identifier)

            elif isinstance(patched, str):

                patched_versions.append(patched)

        #
        # CWEs
        #

        cwes = []

        for cwe in advisory.get("cwes") or []:

            if isinstance(cwe, str):

                cwes.append(cwe)

            elif isinstance(cwe, dict):

                cwe_id = cwe.get("cwe_id")

                if cwe_id:
                    cwes.append(cwe_id)

        #
        # References
        #

        references = []

        for reference in advisory.get("references") or []:

            if isinstance(reference, str):

                references.append(reference)

            elif isinstance(reference, dict):

                url = reference.get("url")

                if url:
                    references.append(url)

        #
        # Remove duplicates while preserving order
        #

        packages = list(dict.fromkeys(packages))

        ecosystems = list(dict.fromkeys(ecosystems))

        patched_versions = list(dict.fromkeys(patched_versions))

        cwes = list(dict.fromkeys(cwes))

        references = list(dict.fromkeys(references))

        #
        # Normalized GitHub intelligence
        #
        # Important:
        # - title preserves GitHub's advisory summary
        # - description preserves the full advisory description
        # - raw preserves the complete original advisory
        #

        return {
            "cve": cve,
            "title": advisory.get("summary"),
            "description": advisory.get("description"),
            "published": advisory.get("published_at"),
            "modified": advisory.get("updated_at"),
            "severity": advisory.get("severity"),
            "cvss": {
                "score": score,
                "vector": vector,
            },
            "cwes": cwes,
            "references": references,
            "technology": {
                "vendors": [],
                "products": [],
                "packages": packages,
                "repositories": [],
                "ecosystems": ecosystems,
                "versions": patched_versions,
            },
            #
            # Complete original GitHub Advisory
            #
            "raw": deepcopy(advisory),
        }


normalizer = GitHubNormalizer()
