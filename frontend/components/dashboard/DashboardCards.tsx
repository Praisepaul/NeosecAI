import MetricCard from "./MetricCard";
import { DashboardSummary } from "@/types/dashboard";

interface Props {
    summary: DashboardSummary;
}

export default function DashboardCards({
    summary,
}: Props) {
    return (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">

            <MetricCard
                title="Total Threats"
                value={summary.total_threats}
                description="Threats currently tracked"
            />

            <MetricCard
                title="Critical Threats"
                value={summary.critical}
                description="Highest severity vulnerabilities"
            />

            <MetricCard
                title="KEV"
                value={summary.kev}
                description="Known Exploited Vulnerabilities"
            />

            <MetricCard
                title="Security Score"
                value={`${summary.security_score}/100`}
                description="Current security posture"
            />

            <MetricCard
                title="High Severity"
                value={summary.high}
            />

            <MetricCard
                title="Medium Severity"
                value={summary.medium}
            />

            <MetricCard
                title="Matched Assets"
                value={summary.matched_assets}
            />

            <MetricCard
                title="Internet-Facing Assets"
                value={summary.internet_facing_assets}
            />

        </div>
    );
}