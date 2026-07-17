import { Threat } from "@/types/threat";


const API_URL =
    "http://127.0.0.1:8000";


export async function getThreats(): Promise<Threat[]> {

    const response = await fetch(
        `${API_URL}/api/threats/`,
        {
            cache: "no-store",
        }
    );


    if (!response.ok) {

        throw new Error(
            "Failed to fetch threat intelligence"
        );

    }


    return response.json();

}