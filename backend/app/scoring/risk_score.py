ASSET_CRITICALITY_WEIGHTS = {
    "CRITICAL": 5,
    "HIGH": 4,
    "MEDIUM": 2,
    "LOW": 1,
}


class RiskScore:

    def calculate(self, finding):

        score = 0

        cvss = finding.get("cvss", {})
        cvss_score = cvss.get("score")

        if cvss_score is not None:
            score += min(cvss_score * 3, 30)

        
        for asset in finding.get("matched_assets", []):

            weight = ASSET_CRITICALITY_WEIGHTS.get(
                str(asset.get("criticality", "")).upper(), 0
            )

            score += weight * 5

            if asset.get("internet_facing", False):
                score += 10

        for product in finding.get("matched_products", []):

            product_criticality = product.get("criticality")

            if isinstance(product_criticality, (int, float)):
                score += product_criticality * 2

            if product.get("internet_facing", False):
                score += 5

        if finding.get("matched"):
            score += 10

        if finding.get("kev", False):
            score += 25

        epss = finding.get("epss")

        if epss:
            score += min(epss.get("score", 0) * 15, 15)

        return min(round(score), 100)


risk_score = RiskScore()
