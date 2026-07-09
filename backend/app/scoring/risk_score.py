class RiskScore:

    def calculate(self, finding):

        score = 0

        cvss = finding.get("cvss", {})

        cvss_score = cvss.get("score")

        if cvss_score is not None:
            score += min(cvss_score * 3, 30)

        if finding.get("matched"):
            score += 20

        for asset in finding.get("matched_assets", []):

            score += asset.get("criticality", 0) * 5

            if asset.get("internet_facing", False):
                score += 10

        if finding.get("kev", False):
            score += 25

        epss = finding.get("epss")

        if epss is not None:
            score += min(float(epss) * 15, 15)

        return min(round(score), 100)


risk_score = RiskScore()