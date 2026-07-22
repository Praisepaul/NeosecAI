from app.enrichers.base_enricher import BaseEnricher
from app.matching.product_matcher import matcher


class ProductEnricher(BaseEnricher):
    """Flags whether a threat affects anything in the technology/product
    inventory (config/technology_inventory.json).

    This is a DIFFERENT concept from AssetMatcher, which matches against
    real, monitored assets (actual hosts/servers/containers). The two
    must never share a field:
      - product-inventory hits -> finding["matched_products"]
      - real-asset hits        -> finding["matched_assets"] (set earlier
                                   by AssetMatcher, never touched here)
    """

    def enrich(self, finding):

        technology = finding.get("technology", {})

        products = technology.get("products", [])

        matches = matcher.match(products)

        finding["matched_products"] = matches

        finding["matched"] = finding.get("matched", False) or len(matches) > 0

        finding["metadata"]["matched_products"] = matches
        finding["metadata"]["matched"] = finding["matched"]

        return finding


product_enricher = ProductEnricher()
