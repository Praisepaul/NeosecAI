import json
from pathlib import Path

CONFIG = (
    Path(__file__)
    .parent.parent
    / "config"
    / "technology_inventory.json"
)


class ProductMatcher:

    def __init__(self):

        with open(CONFIG, encoding="utf-8") as f:
            self.inventory = json.load(f)["products"]

    def match(self, products):

        matches = []

        normalized_products = [
            p.lower()
            for p in products
        ]

        for technology in self.inventory:

            aliases = [
                a.lower()
                for a in technology["aliases"]
            ]

            if any(
                alias in normalized_products
                for alias in aliases
            ):
                matches.append(technology)

        return matches


matcher = ProductMatcher()