from app.enrichers.base_enricher import BaseEnricher
from app.collectors.epss_collector import collector as epss_collector


class EPSSEnricher(BaseEnricher):

    def enrich(self, finding):

        result = epss_collector.collect([finding["cve"]])

        if finding["cve"] in result:

            finding["epss"] = {

                "score": result[finding["cve"]]["epss"],

                "percentile": result[finding["cve"]]["percentile"]

            }

        else:

            finding["epss"] = None

        return finding


epss_enricher = EPSSEnricher()