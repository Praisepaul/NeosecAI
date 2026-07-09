from app.repositories.threat_repository import threat_repository


class DashboardService:

    def summary(self):

        threats = threat_repository.get_all()

        total = len(threats)

        critical = 0
        high = 0
        medium = 0
        low = 0

        matched = 0

        average_score = 0

        for threat in threats:

            severity = threat.get("severity", "").upper()

            if severity == "CRITICAL":
                critical += 1

            elif severity == "HIGH":
                high += 1

            elif severity == "MEDIUM":
                medium += 1

            elif severity == "LOW":
                low += 1

            if threat.get("matched"):
                matched += 1

            if threat.get("risk_score"):
                average_score += threat["risk_score"]

        if total:

            average_score /= total

        return {

            "total": total,

            "critical": critical,

            "high": high,

            "medium": medium,

            "low": low,

            "matched": matched,

            "averageRisk": round(average_score, 2)
        }


dashboard_service = DashboardService()