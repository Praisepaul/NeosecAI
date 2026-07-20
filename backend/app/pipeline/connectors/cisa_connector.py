from app.collectors.cisa_collector import collector


class CISAConnector:

    def collect(self, cves):

        raw = collector.collect()

        print(f"[CISA] Loaded {len(raw)} KEV vulnerabilities")

        # Normalize CVE IDs for safe comparison
        kev_cves = {cve.strip().upper() for cve in raw.keys()}

        nvd_cves = {cve.strip().upper() for cve in cves}

        matches = {cve: raw[cve] for cve in raw if cve.strip().upper() in nvd_cves}

        print(f"[CISA] Matches in current NVD batch: {len(matches)}")

        if matches:

            print("[CISA] Matching CVEs:")

            for cve, vuln in matches.items():

                print(f"  - {cve}: " f"{vuln.get('vulnerabilityName')}")

        else:

            print("[CISA] No matching CVEs found.")

        return matches


cisa_connector = CISAConnector()
