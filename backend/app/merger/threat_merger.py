from copy import deepcopy


class ThreatMerger:
    """
    Builds a single canonical threat document from multiple normalized sources.

    Responsibilities:
        1. Build base threat document
        2. Preserve all source intelligence
        3. Merge descriptive fields
        4. Merge CVSS
        5. Merge technologies
        6. Merge references
        7. Merge weaknesses (CWEs)
        8. Prepare metadata
        9. Cleanup and deduplicate
    """

    # ==========================================================
    # PUBLIC ENTRY POINT
    # ==========================================================

    def merge(
        self,
        nvd=None,
        github=None,
        cisa=None,
        epss=None,
    ):

        threat = self._build_base_document()

        self._store_sources(threat, nvd, github, cisa, epss)

        self._merge_descriptions(threat, nvd, github, cisa)

        self._merge_cvss(threat, nvd, github)

        self._merge_technology(threat, nvd, github)

        self._merge_references(threat, nvd, github, cisa)

        self._merge_cwes(threat, nvd, github)

        self._merge_metadata(threat, epss)

        self._cleanup(threat)

        return threat

    # ==========================================================

    # HELPER FUNCTIONS
    # ==========================================================

    def _unique(self, values):
        """
        Removes duplicates while preserving order.
        Ignores None and empty strings.
        """
        seen = set()
        result = []

        for value in values:

            if value is None:
                continue

            if isinstance(value, str):
                value = value.strip()

                if not value:
                    continue

            key = str(value)

            if key not in seen:
                seen.add(key)
                result.append(value)

        return result

    def _merge_lists(self, *lists):
        """
        Merge multiple lists into one unique list.
        """

        merged = []

        for lst in lists:

            if isinstance(lst, list):
                merged.extend(lst)

        return self._unique(merged)

    def _merge_dict(self, primary, secondary):
        """
        Merge two dictionaries.
        Primary values win.
        Missing fields are copied from secondary.
        """

        result = deepcopy(primary or {})

        for key, value in (secondary or {}).items():

            if key not in result or result[key] in [None, "", [], {}]:
                result[key] = deepcopy(value)

        return result

    # ==========================================================
    # STEP 1
    # ==========================================================

    def _build_base_document(self):

        return {
            "cve": None,
            "title": None,
            "summary": None,
            "description": None,
            "published": None,
            "modified": None,
            "cvss": {},
            "epss": {},
            "kev": False,
            "kev_details": None,
            "risk_score": 0,
            "references": [],
            "cwes": [],
            "technology": {
                "vendors": [],
                "products": [],
                "packages": [],
                "repositories": [],
                "ecosystems": [],
                "versions": [],
            },
            "sources": {"nvd": None, "github": None, "cisa": None, "epss": None},
            "metadata": {
                "matched": False,
                "matched_assets": [],
                "exploit_available": False,
                "last_synced": None,
            },
        }

    # ==========================================================
    # STEP 2
    # ==========================================================

    def _store_sources(self, threat, nvd, github, cisa, epss):

        threat["sources"]["nvd"] = deepcopy(nvd)

        threat["sources"]["github"] = deepcopy(github)

        threat["sources"]["cisa"] = deepcopy(cisa)

        threat["sources"]["epss"] = deepcopy(epss)

    # ==========================================================
    # STEP 3
    # ==========================================================

    def _merge_descriptions(self, threat, nvd, github, cisa):

        # Priority:
        # Vendor -> GitHub -> NVD
        # (Vendor support will come later)

        primary = github or nvd or {}

        threat["cve"] = (nvd or github or {}).get("cve")

        threat["title"] = (nvd or github or {}).get("title")

        threat["summary"] = primary.get("summary")

        threat["description"] = primary.get("description")

        threat["published"] = (nvd or github or {}).get("published")

        threat["modified"] = (nvd or github or {}).get("modified")

    # ==========================================================
    # STEP 4
    # ==========================================================

    def _merge_cvss(self, threat, nvd, github):

        if nvd and nvd.get("cvss"):

            threat["cvss"] = deepcopy(nvd["cvss"])

        elif github and github.get("cvss"):

            threat["cvss"] = deepcopy(github["cvss"])

    # ==========================================================
    # STEP 5
    # ==========================================================

    def _merge_technology(
        self,
        threat,
        nvd,
        github
    ):

        nvd_tech = (nvd or {}).get("technology", {})
        github_tech = (github or {}).get("technology", {})

        technology = {

            "vendors": self._merge_lists(
                nvd_tech.get("vendors"),
                github_tech.get("vendors")
            ),

            "products": self._merge_lists(
                nvd_tech.get("products"),
                github_tech.get("products")
            ),

            "packages": self._merge_lists(
                nvd_tech.get("packages"),
                github_tech.get("packages")
            ),

            "repositories": self._merge_lists(
                nvd_tech.get("repositories"),
                github_tech.get("repositories")
            ),

            "ecosystems": self._merge_lists(
                nvd_tech.get("ecosystems"),
                github_tech.get("ecosystems")
            ),

            "versions": self._merge_lists(
                nvd_tech.get("versions"),
                github_tech.get("versions")
            )

        }

        threat["technology"] = technology

    # ==========================================================
    # STEP 6
    # ==========================================================

    def _merge_references(
        self,
        threat,
        nvd,
        github,
        cisa
    ):

        references = self._merge_lists(

            (nvd or {}).get("references"),

            (github or {}).get("references"),

            (cisa or {}).get("references")

        )

        threat["references"] = sorted(references)

    # ==========================================================
    # STEP 7
    # ==========================================================

    def _merge_cwes(
        self,
        threat,
        nvd,
        github
    ):

        threat["cwes"] = sorted(

            self._merge_lists(

                (nvd or {}).get("cwes"),

                (github or {}).get("cwes")

            )

        )

    # ==========================================================
    # STEP 8
    # ==========================================================

    def _merge_metadata(self, threat, epss):

        if epss:

            threat["epss"] = deepcopy(epss)

    # ==========================================================
    # STEP 9
    # ==========================================================

    def _cleanup(
        self,
        threat
    ):

        threat["references"] = self._unique(
            threat.get("references", [])
        )

        threat["cwes"] = self._unique(
            threat.get("cwes", [])
        )

        tech = threat.get("technology", {})

        for field in tech:

            tech[field] = self._unique(
                tech.get(field, [])
            )


merger = ThreatMerger()
