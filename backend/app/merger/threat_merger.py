from copy import deepcopy


class ThreatMerger:

    def merge(
        self,
        nvd=None,
        github=None,
        cisa=None,
        epss=None,
    ):

        threat = self._build_base_document()

        self._store_sources(
            threat,
            nvd,
            github,
            cisa,
            epss,
        )

        self._merge_identity(
            threat,
            nvd,
            github,
        )

        self._merge_content(
            threat,
            nvd,
            github,
        )

        self._merge_dates(
            threat,
            nvd,
            github,
        )

        self._merge_cvss(
            threat,
            nvd,
            github,
        )

        self._merge_kev(
            threat,
            cisa,
        )

        self._merge_technology(
            threat,
            nvd,
            github,
        )

        self._merge_references(
            threat,
            nvd,
            github,
            cisa,
        )

        self._merge_cwes(
            threat,
            nvd,
            github,
        )

        self._merge_epss(
            threat,
            epss,
        )

        self._cleanup(threat)

        return threat

    # ==========================================================
    # BASE DOCUMENT
    # ==========================================================

    def _build_base_document(self):

        return {
            "cve": None,
            "title": None,
            "description": None,
            "published": None,
            "modified": None,
            "cvss": {},
            "epss": None,
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
            "sources": {
                "nvd": None,
                "github": None,
                "cisa": None,
                "epss": None,
            },
            "metadata": {
                "matched": False,
                "matched_assets": [],
                "exploit_available": False,
                "last_synced": None,
            },
        }

    # ==========================================================
    # PRESERVE SOURCES
    # ==========================================================

    def _store_sources(
        self,
        threat,
        nvd,
        github,
        cisa,
        epss,
    ):

        threat["sources"]["nvd"] = deepcopy(nvd)

        threat["sources"]["github"] = deepcopy(github)

        threat["sources"]["cisa"] = deepcopy(cisa)

        threat["sources"]["epss"] = deepcopy(epss)

    # ==========================================================
    # IDENTITY
    # ==========================================================

    def _merge_identity(
        self,
        threat,
        nvd,
        github,
    ):

        threat["cve"] = (nvd or {}).get("cve") or (github or {}).get("cve")

    # ==========================================================
    # TITLE AND DESCRIPTION
    # ==========================================================

    def _merge_content(
        self,
        threat,
        nvd,
        github,
    ):

        github_title = (github or {}).get("title")

        github_description = (github or {}).get("description")

        nvd_description = (nvd or {}).get("description")

        #
        # GitHub Advisory is the preferred
        # human-readable source when available.
        #

        if github_title:
            threat["title"] = github_title
            threat["description"] = github_description or github_title
            return

        if nvd_description:
            threat["title"] = nvd_description
            threat["description"] = nvd_description
            return

        if github_description:
            threat["title"] = github_description
            threat["description"] = github_description

    # ==========================================================
    # DATES
    # ==========================================================

    def _merge_dates(
        self,
        threat,
        nvd,
        github,
    ):

        threat["published"] = (nvd or {}).get("published") or (github or {}).get(
            "published"
        )

        threat["modified"] = (nvd or {}).get("modified") or (github or {}).get(
            "modified"
        )

    # ==========================================================
    # CVSS
    # ==========================================================

    def _merge_cvss(
        self,
        threat,
        nvd,
        github,
    ):

        nvd_cvss = (nvd or {}).get("cvss")

        github_cvss = (github or {}).get("cvss")

        if nvd_cvss:

            threat["cvss"] = deepcopy(nvd_cvss)

        elif github_cvss:

            threat["cvss"] = deepcopy(github_cvss)

    # ==========================================================
    # CISA KEV
    # ==========================================================

    # ==========================================================
# CISA KEV
# ==========================================================


    def _merge_kev(
        self,
        threat,
        cisa,
    ):
    
        if not cisa:
        
            return
    
        threat["kev"] = cisa.get(
            "kev",
            False,
        )
    
        threat["kev_details"] = deepcopy(cisa.get("kev_details"))

    # ==========================================================
    # TECHNOLOGY
    # ==========================================================

    def _merge_technology(
        self,
        threat,
        nvd,
        github,
    ):

        nvd_technology = (nvd or {}).get("technology") or {}

        github_technology = (github or {}).get("technology") or {}

        threat["technology"] = {
            "vendors": self._merge_lists(
                nvd_technology.get("vendors"),
                github_technology.get("vendors"),
            ),
            "products": self._merge_lists(
                nvd_technology.get("products"),
                github_technology.get("products"),
            ),
            "packages": self._merge_lists(
                nvd_technology.get("packages"),
                github_technology.get("packages"),
            ),
            "repositories": self._merge_lists(
                nvd_technology.get("repositories"),
                github_technology.get("repositories"),
            ),
            "ecosystems": self._merge_lists(
                nvd_technology.get("ecosystems"),
                github_technology.get("ecosystems"),
            ),
            "versions": self._merge_lists(
                nvd_technology.get("versions"),
                github_technology.get("versions"),
            ),
        }

    # ==========================================================
    # REFERENCES
    # ==========================================================

    def _merge_references(
        self,
        threat,
        nvd,
        github,
        cisa,
    ):

        threat["references"] = self._merge_lists(
            (nvd or {}).get("references"),
            (github or {}).get("references"),
            (cisa or {}).get("references"),
        )

    # ==========================================================
    # CWEs
    # ==========================================================

    def _merge_cwes(
        self,
        threat,
        nvd,
        github,
    ):

        threat["cwes"] = self._merge_lists(
            (nvd or {}).get("cwes"),
            (github or {}).get("cwes"),
        )

    # ==========================================================
    # EPSS
    # ==========================================================

    def _merge_epss(
        self,
        threat,
        epss,
    ):

        if epss:

            threat["epss"] = deepcopy(epss)

    # ==========================================================
    # HELPERS
    # ==========================================================

    def _merge_lists(
        self,
        *lists,
    ):

        values = []

        for value_list in lists:

            if not isinstance(
                value_list,
                list,
            ):

                continue

            values.extend(value_list)

        return self._unique(values)

    def _unique(
        self,
        values,
    ):

        result = []

        seen = set()

        for value in values:

            if value is None:

                continue

            if isinstance(
                value,
                str,
            ):

                value = value.strip()

                if not value:

                    continue

            key = str(value)

            if key in seen:

                continue

            seen.add(key)

            result.append(value)

        return result

    # ==========================================================
    # CLEANUP
    # ==========================================================

    def _cleanup(
        self,
        threat,
    ):

        threat["references"] = self._unique(
            threat.get(
                "references",
                [],
            )
        )

        threat["cwes"] = self._unique(
            threat.get(
                "cwes",
                [],
            )
        )

        technology = threat.get(
            "technology",
            {},
        )

        for field in technology:

            technology[field] = self._unique(
                technology.get(
                    field,
                    [],
                )
            )


merger = ThreatMerger()
