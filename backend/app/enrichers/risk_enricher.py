from app.enrichers.base_enricher import BaseEnricher
from app.scoring.risk_score import risk_score


class RiskEnricher(BaseEnricher):

    def enrich(self, finding):

        finding["risk_score"] = risk_score.calculate(finding)

        return finding


risk_enricher = RiskEnricher()