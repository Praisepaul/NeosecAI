export interface CVSS {
    version?: string | null;
    severity?: string | null;
    score?: number | null;
    vector?: string | null;
}

export interface EPSS {
    score?: number | null;
    percentile?: number | null;
}

export interface ThreatSummary {
    cve: string;

    title?: string | null;

    published?: string | null;

    modified?: string | null;

    cvss?: CVSS | null;

    epss?: EPSS | null;

    kev?: boolean;

    risk_score?: number;

    matched?: boolean;

    matched_assets?: MatchedAsset[];

    matched_products?: MatchedProduct[];
}

export interface Threat extends ThreatSummary {
    description?: string | null;

    kev_details?: KevDetails | null;

    references?: string[];

    cwes?: string[];

    technology?: Technology;

    sources?: ThreatSources;

    metadata?: ThreatMetadata;
}

/**
 * A REAL, monitored asset (host/server/container) that this threat
 * affects. Comes from AssetMatcher on the backend - do not confuse
 * with MatchedProduct below.
 */
export interface MatchedAsset {
    hostname: string;
    criticality: string; // "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    internet_facing: boolean;
    score: number;
    matched_on: string[];
}

/**
 * A product in the technology inventory (config/technology_inventory.json)
 * that this threat affects. Comes from ProductEnricher on the backend -
 * this is NOT a confirmed hit on a real asset.
 */
export interface MatchedProduct {
    name: string;
    aliases?: string[];
    criticality?: number; // 1-5 scale, defined in the inventory file
    internet_facing?: boolean;
}

export interface Technology {
    vendors?: string[];
    products?: string[];
    packages?: string[];
    repositories?: string[];
    ecosystems?: string[];
    versions?: string[];
}

// Raw, source-specific payloads. Shape varies per-source and is large/
// dynamic (full NVD CVE record, full GitHub advisory, etc) - typed as
// an open record instead of `any` so callers still can't do unchecked
// property access without acknowledging the value is unknown-shaped.
export type RawSourceData = Record<string, unknown>;

export interface ThreatSources {
    nvd?: RawSourceData | null;
    github?: RawSourceData | null;
    cisa?: RawSourceData | null;
    epss?: EPSS | null;
}

export interface KevDetails {
    vendor_project?: string | null;
    product?: string | null;
    vulnerability_name?: string | null;
    date_added?: string | null;
    short_description?: string | null;
    required_action?: string | null;
    due_date?: string | null;
    known_ransomware_campaign_use?: string | null;
    notes?: string | null;
}

export interface ThreatMetadata {
    matched?: boolean;
    matched_assets?: MatchedAsset[];
    matched_products?: MatchedProduct[];
    exploit_available?: boolean;
    last_synced?: string | null;
}
