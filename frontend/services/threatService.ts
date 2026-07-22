import { api } from "@/lib/api";
import { Threat, ThreatSummary } from "@/types/threat";

export interface SyncResult {
    status: string;
    collector: string;
    downloaded: number;
    stored: number;
    started: string;
    finished: string;
}

export async function getThreats(): Promise<ThreatSummary[]> {
    const response = await api.get<ThreatSummary[]>(
        "/api/threats/",
    );

    return response.data;
}

export async function getThreatByCve(
    cve: string,
): Promise<Threat> {
    const response = await api.get<Threat>(
        `/api/threats/${encodeURIComponent(cve)}`,
    );

    return response.data;
}

export async function syncThreats(): Promise<SyncResult> {
    // A sync can legitimately take a while (NVD paging + GitHub/CISA/EPSS
    // lookups), so it gets a much longer timeout than the default 30s
    // used for normal reads.
    const response = await api.post<SyncResult>("/api/threats/sync", null, {
        timeout: 5 * 60 * 1000,
    });

    return response.data;
}
