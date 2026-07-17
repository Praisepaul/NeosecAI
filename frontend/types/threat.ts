export interface CVSS {
    version: string;
    severity: string;
    score: number;
    vector: string;
}

export interface EPSS {
    score: number;
    percentile: number;
}

export interface Technology {
    vendors: string[];
    products: string[];
    packages: string[];
    repositories: string[];
    ecosystems: string[];
    versions: string[];
}

export interface ThreatMetadata {
    matched: boolean;
    matched_assets: string[];
    exploit_available: boolean;
    last_synced: string | null;
}

export interface ThreatSources {
    nvd: unknown | null;
    github: unknown | null;
    cisa: unknown | null;
    epss: EPSS | null;
}

export interface Threat {
    cve: string;

    title: string;

    summary: string | null;

    description: string | null;

    published: string | null;

    modified: string | null;

    cvss: CVSS;

    epss: EPSS | null;

    kev: boolean;

    kev_details: unknown | null;

    risk_score: number;

    cwes: string[];

    references: string[];

    matched: boolean;

    matched_assets: string[];

    metadata: ThreatMetadata;

    technology: Technology;

    sources: ThreatSources;
}