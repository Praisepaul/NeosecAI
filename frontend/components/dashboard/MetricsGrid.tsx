import DashboardCards from "./DashboardCards";
import { DashboardResponse } from "@/types/dashboard";

interface Props {
    dashboard: DashboardResponse;
}

export default function MetricsGrid({
    dashboard,
}: Props) {
    return (
        <DashboardCards summary={dashboard.summary} />
    );
}