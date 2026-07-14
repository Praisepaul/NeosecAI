"""
Threat Merger
=============

Responsible for building ONE canonical threat record from multiple
intelligence sources.

Responsibilities
----------------
✔ Never overwrite high-confidence NVD information unless missing.
✔ Merge complementary intelligence from other providers.
✔ Remove duplicate values.
✔ Preserve ordering where appropriate.
✔ Produce ONE clean threat object.

Current Sources
---------------
- NVD (Primary)
- GitHub Security Advisories

Future Sources
--------------
- CISA KEV
- EPSS
- ExploitDB
- VulDB
- Microsoft MSRC
- Snyk
- Rapid7
- Tenable
- CrowdStrike
- VulnCheck
"""


from copy import deepcopy


class ThreatMerger:

    # ==========================================================
    # Public API
    # ==========================================================

    def merge(
        self,
        nvd: dict,
        github: dict | None = None,
        cisa: dict | None = None,
        epss: dict | None = None,
        exploitdb: dict | None = None,
    ):

        """
        Merge every intelligence source into a single
        canonical threat object.
        """

        threat = deepcopy(nvd)

        #
        # Merge GitHub
        #

        if github:
            self._merge_github(threat, github)

        #
        # Future
        #

        if cisa:
            pass

        if epss:
            pass

        if exploitdb:
            pass

        return threat

    # ==========================================================
    # GitHub
    # ==========================================================

    def _merge_github(self, threat, github):

        #
        # Preserve original advisory
        #

        threat.setdefault("advisories", {})
        threat["advisories"]["github"] = github

        #
        # Prefer NVD title
        #

        if not threat.get("title"):
            threat["title"] = github.get("summary")

        #
        # Prefer NVD summary
        #

        if not threat.get("summary"):
            threat["summary"] = github.get("summary")

        #
        # Prefer NVD description
        #

        if not threat.get("description"):
            threat["description"] = github.get("description")

        #
        # Published
        # Keep earliest known publication date
        #

        threat["published"] = self._earliest_date(
            threat.get("published"),
            github.get("published")
        )

        #
        # Modified
        # Keep latest modification date
        #

        threat["modified"] = self._latest_date(
            threat.get("modified"),
            github.get("updated")
        )

        #
        # CVSS
        # NVD always wins
        #

        if not threat.get("cvss", {}).get("score"):

            threat["cvss"] = github.get("cvss", {})

        #
        # Severity
        # NVD always wins
        #

        if not threat.get("cvss", {}).get("severity"):

            github_severity = github.get("severity")

            if github_severity:

                threat.setdefault("cvss", {})

                threat["cvss"]["severity"] = github_severity

        #
        # References
        #

        threat["references"] = self._unique(
            threat.get("references", [])
            + github.get("references", [])
        )

        #
        # CWEs
        #

        threat.setdefault("weaknesses", {})

        threat["weaknesses"]["cwes"] = self._unique(
            threat.get("weaknesses", {}).get("cwes", [])
            + github.get("cwes", [])
        )

        #
        # Technology
        #

        technology = threat.setdefault("technology", {})

        technology["packages"] = self._union(
            technology.get("packages"),
            github.get("packages")
        )

        technology["ecosystems"] = self._union(
            technology.get("ecosystems"),
            github.get("ecosystems")
        )

        technology["repositories"] = self._union(
            technology.get("repositories"),
            github.get("repositories")
        )

        technology["patched_versions"] = self._union(
            technology.get("patched_versions"),
            github.get("patched_versions")
        )

    # ==========================================================
    # Generic Helpers
    # ==========================================================

    def _union(self, a, b):

        """
        Merge two lists.

        Remove duplicates.

        Return sorted output.
        """

        a = a or []
        b = b or []

        return sorted(set(a + b))

    def _unique(self, values):

        """
        Remove duplicates while preserving order.
        """

        values = values or []

        return list(dict.fromkeys(values))

    def _earliest_date(self, first, second):

        """
        Keep earliest date.
        """

        if not first:
            return second

        if not second:
            return first

        return min(first, second)

    def _latest_date(self, first, second):

        """
        Keep latest date.
        """

        if not first:
            return second

        if not second:
            return first

        return max(first, second)


merger = ThreatMerger()