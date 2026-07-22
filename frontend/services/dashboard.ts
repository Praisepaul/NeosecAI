import { api } from "@/lib/api";
import { DashboardResponse } from "@/types/dashboard";

export async function getDashboard(): Promise<DashboardResponse> {
    // NOTE: backend only mounts this under /api now (the old duplicate
    // mount directly on `/dashboard` was removed on the backend side -
    // this call must include the /api prefix or it will 404).
    const response = await api.get<DashboardResponse>("/api/dashboard/");

    return response.data;
}
