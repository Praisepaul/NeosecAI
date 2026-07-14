from app.enrichers.base_enricher import BaseEnricher
from app.collectors.cisa_collector import collector as cisa_collector


class CISAEnricher(BaseEnricher):

    def __init__(self):
        self.kev = None

    def enrich(self, finding):

        # Download KEV catalog only once
        if self.kev is None:
            self.kev = cisa_collector.collect()

        kev = self.kev.get(finding["cve"])

        if kev:

            finding["kev"] = True

            finding["kev_details"] = {

                "date_added": kev.get("dateAdded"),

                "vendor": kev.get("vendorProject"),

                "product": kev.get("product"),

                "required_action": kev.get("requiredAction"),

                "due_date": kev.get("dueDate"),

                "known_ransomware": kev.get("knownRansomwareCampaignUse")

            }

        else:

            finding["kev"] = False

            finding["kev_details"] = None

        return finding


cisa_enricher = CISAEnricher()