export async function fetchFromFlask(endpoint: string) {
    const flaskURL = import.meta.env.VITE_FLASK_URL;
    const response = await fetch(`${flaskURL}/${endpoint}`);

    if (!response.ok) {
        throw new Error(`Failed to fetch from Flask API: ${response.status}`);
    }

    return response.json();
}