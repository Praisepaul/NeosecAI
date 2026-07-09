from app.enrichers.base_enricher import BaseEnricher
from app.matching.product_matcher import matcher


class ProductEnricher(BaseEnricher):

    def enrich(self, finding):

        technology = finding.get("technology", {})

        products = technology.get("products", [])

        matches = matcher.match(products)

        finding["matched"] = len(matches) > 0

        finding["matched_assets"] = matches

        return finding


product_enricher = ProductEnricher()