import { api } from "@/lib/api";
import { DashboardResponse } from "@/types/dashboard";

export async function getDashboard(): Promise<DashboardResponse> {
    const response = await api.get<DashboardResponse>("/dashboard/");

    return response.data;
}