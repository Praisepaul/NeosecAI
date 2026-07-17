from app.core.database import db


class DashboardService:

    COLLECTION = "threats"

    def get_dashboard(self):

        threats = db[self.COLLECTION]

        total = threats.count_documents({})

        critical = threats.count_documents({"cvss.severity": "CRITICAL"})
        high = threats.count_documents({"cvss.severity": "HIGH"})
        medium = threats.count_documents({"cvss.severity": "MEDIUM"})
        low = threats.count_documents({"cvss.severity": "LOW"})

        kev = threats.count_documents({"kev": True})

        matched_assets = threats.count_documents({"matched": True})

        internet_facing = db["assets"].count_documents({"internet_facing": True})

        #
        # Top Vendors
        #

        vendor_pipeline = [
            {"$unwind": "$technology.vendors"},
            {"$group": {"_id": "$technology.vendors", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10},
        ]

        vendors = []

        for vendor in threats.aggregate(vendor_pipeline):

            vendors.append({"vendor": vendor["_id"], "count": vendor["count"]})

        #
        # Recent Threats
        #

        recent = list(
            threats.find(
                {},
                {
                    "_id": 0,
                    "cve": 1,
                    "title": 1,
                    "cvss": 1,
                    "published": 1,
                    "risk_score": 1,
                },
            )
            .sort("published", -1)
            .limit(10)
        )

        #
        # Security Score
        #

        security_score = max(0, 100 - (critical * 5) - (high * 2) - kev)

        return {
            "summary": {
                "total_threats": total,
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low,
                "kev": kev,
                "matched_assets": matched_assets,
                "internet_facing_assets": internet_facing,
                "security_score": security_score,
            },
            "severity_distribution": {
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low,
            },
            "top_vendors": vendors,
            "recent_threats": recent,
        }


dashboard_service = DashboardService()
