const API = "http://127.0.0.1:8000/api";

export async function getDashboard() {
    const response = await fetch(`${API}/dashboard/`);

    if (!response.ok) {
        throw new Error("Failed to load dashboard");
    }

    return response.json();
}