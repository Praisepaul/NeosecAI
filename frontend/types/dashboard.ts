
export interface DashboardSummary {
    total_threats: number;
    critical: number;
    high: number;
    medium: number;
    low: number;
    kev: number;
    matched_assets: number;
    internet_facing_assets: number;
    security_score: number;
}

export interface SeverityDistribution {
    critical: number;
    high: number;
    medium: number;
    low: number;
}

export interface TopVendor {
    vendor: string;
    count: number;
}


export interface DashboardResponse {
    summary: DashboardSummary;
    severity_distribution: SeverityDistribution;
    top_vendors: TopVendor[];
}