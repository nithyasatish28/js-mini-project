const API_URL = "http://127.0.0.1:8000";

export async function getPlants() {
    const response = await fetch(`${API_URL}/plants`);

    if (!response.ok) {
        throw new Error("Failed to fetch plants");
    }

    return response.json();
}