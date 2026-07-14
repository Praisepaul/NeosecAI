from app.enrichers.epss_enricher import epss_enricher
from app.enrichers.cisa_enricher import cisa_enricher
from app.enrichers.product_enricher import product_enricher
from app.enrichers.risk_enricher import risk_enricher


class EnrichmentEngine:

    def __init__(self):

        self.pipeline = [

            epss_enricher,

            cisa_enricher,

            product_enricher,

            risk_enricher,

        ]

    def enrich(self, finding):

        for enricher in self.pipeline:

            finding = enricher.enrich(finding)

        return finding


engine = EnrichmentEngine()