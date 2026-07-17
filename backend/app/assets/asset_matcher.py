from app.assets.asset_repository import asset_repository


class AssetMatcher:

    def match(self, threat):

        technology = threat.get("technology", {})

        threat_products = {p.lower() for p in technology.get("products", [])}

        threat_vendors = {v.lower() for v in technology.get("vendors", [])}

        threat_packages = {p.lower() for p in technology.get("packages", [])}

        threat_repositories = {r.lower() for r in technology.get("repositories", [])}

        matched_assets = []

        assets = asset_repository.get_all()

        for asset in assets:

            score = 0
            matched_on = []

            #
            # Vendor
            #

            if asset.get("vendor", "").lower() in threat_vendors:
                score += 3
                matched_on.append("vendor")

            #
            # Products
            #

            asset_products = {p.lower() for p in asset.get("products", [])}

            if threat_products & asset_products:
                score += 5
                matched_on.append("product")

            #
            # Packages
            #

            asset_packages = {p.lower() for p in asset.get("packages", [])}

            if threat_packages & asset_packages:
                score += 4
                matched_on.append("package")

            #
            # Repositories
            #

            asset_repositories = {r.lower() for r in asset.get("repositories", [])}

            if threat_repositories & asset_repositories:
                score += 4
                matched_on.append("repository")

            #
            # Save only matched assets
            #

            if score > 0:

                matched_assets.append(
                    {
                        "hostname": asset["hostname"],
                        "criticality": asset["criticality"],
                        "internet_facing": asset["internet_facing"],
                        "score": score,
                        "matched_on": matched_on,
                    }
                )

        #
        # Highest scoring first
        #

        matched_assets.sort(
            key=lambda asset: asset["score"],
            reverse=True,
        )

        threat["matched"] = len(matched_assets) > 0

        threat["matched_assets"] = matched_assets

        threat["metadata"]["matched"] = threat["matched"]

        threat["metadata"]["matched_assets"] = matched_assets

        return threat


asset_matcher = AssetMatcher()
