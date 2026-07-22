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

export interface MatchedAsset {
    name: string;
    aliases?: string[];
    criticality?: number;
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

export interface ThreatSources {
    nvd?: any;
    github?: any;
    cisa?: any;
    epss?: EPSS | null;
}

export interface Threat {
    cve: string;

    title?: string | null;

    description?: string | null;

    published?: string | null;

    modified?: string | null;

    cvss?: CVSS | null;

    epss?: EPSS | null;

    kev?: boolean;

    kev_details?: any;

    risk_score?: number;

    references?: string[];

    cwes?: string[];

    technology?: Technology;

    matched?: boolean;

    matched_assets?: MatchedAsset[];

    sources?: ThreatSources;

    metadata?: {
        matched?: boolean;
        matched_assets?: MatchedAsset[];
        exploit_available?: boolean;
        last_synced?: string | null;
    };
}