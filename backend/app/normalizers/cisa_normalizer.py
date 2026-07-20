from copy import deepcopy


class CISANormalizer:

    def normalize(self, vuln):

        if not vuln:

            return None

        return {
            "kev": True,
            "kev_details": {
                "vendor_project": vuln.get("vendorProject"),
                "product": vuln.get("product"),
                "vulnerability_name": vuln.get("vulnerabilityName"),
                "date_added": vuln.get("dateAdded"),
                "short_description": vuln.get("shortDescription"),
                "required_action": vuln.get("requiredAction"),
                "due_date": vuln.get("dueDate"),
                "known_ransomware_campaign_use": vuln.get("knownRansomwareCampaignUse"),
                "notes": vuln.get("notes"),
            },
            "references": [],
            "raw": deepcopy(vuln),
        }


normalizer = CISANormalizer()
