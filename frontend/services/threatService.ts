import { Threat } from "@/types/threat";

const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_URL ||
    "http://127.0.0.1:8000";

export async function getThreats(): Promise<Threat[]> {

    const response = await fetch(
        `${API_BASE_URL}/api/threats/`,
        {
            method: "GET",
            headers: {
                Accept: "application/json",
            },
            cache: "no-store",
        }
    );

    if (!response.ok) {
        throw new Error(
            `Failed to fetch threats: ${response.status}`
        );
    }

    return response.json();
}