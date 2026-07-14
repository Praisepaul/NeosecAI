from app.normalizers.base_normalizer import BaseNormalizer


class GitHubNormalizer(BaseNormalizer):

    def normalize(self, advisories):

        if not advisories:
            return None

        advisory = advisories[0]

        cvss = advisory.get("cvss") or {}

        vulnerabilities = advisory.get("vulnerabilities") or []

        packages = []
        ecosystems = []
        patched_versions = []

        #
        # Vulnerabilities
        #

        for vuln in vulnerabilities:

            if not isinstance(vuln, dict):
                continue

            #
            # Package
            #

            package = vuln.get("package")

            if isinstance(package, dict):

                name = package.get("name")
                ecosystem = package.get("ecosystem")

                if name:
                    packages.append(name)

                if ecosystem:
                    ecosystems.append(ecosystem)

            #
            # First patched version
            #

            patched = vuln.get("first_patched_version")

            identifier = None

            if isinstance(patched, dict):
                identifier = patched.get("identifier")

            elif isinstance(patched, str):
                identifier = patched

            if identifier:
                patched_versions.append(identifier)

        #
        # CWEs
        #

        cwes = []

        for cwe in advisory.get("cwes", []):

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

        for ref in advisory.get("references", []):

            if isinstance(ref, str):

                references.append(ref)

            elif isinstance(ref, dict):

                url = ref.get("url")

                if url:
                    references.append(url)

        #
        # CVSS
        #

        score = None
        vector = None

        if isinstance(cvss, dict):
            score = cvss.get("score")
            vector = cvss.get("vector_string")

        return {

            "published": advisory.get("published_at"),

            "updated": advisory.get("updated_at"),

            "severity": advisory.get("severity"),

            "summary": advisory.get("summary"),

            "description": advisory.get("description"),

            "cvss": {

                "score": score,

                "vector": vector

            },

            "cwes": sorted(set(cwes)),

            "references": sorted(set(references)),

            "packages": sorted(set(packages)),

            "ecosystems": sorted(set(ecosystems)),

            "patched_versions": sorted(set(patched_versions))

        }


normalizer = GitHubNormalizer()