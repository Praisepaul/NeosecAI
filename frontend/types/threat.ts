export interface CVSS {

    version: string | null;

    severity: string | null;

    score: number | null;

    vector: string | null;

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


export interface ThreatSource {

    [key: string]: any;

}


export interface Threat {

    cve: string;

    title: string | null;

    summary: string | null;

    description: string | null;

    published: string | null;

    modified: string | null;

    cvss: CVSS;

    epss: EPSS | null;

    kev: boolean;

    kev_details: any;

    risk_score: number;

    references: string[];

    cwes: string[];

    technology: Technology;

    matched: boolean;

    matched_assets: string[];

    metadata: ThreatMetadata;

    sources: {

        nvd: ThreatSource | null;

        github: ThreatSource | null;

        cisa: ThreatSource | null;

        epss: ThreatSource | null;

    };

}