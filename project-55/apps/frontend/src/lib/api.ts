//GET
export async function fetchFromFlask(endpoint: string) {
    const flaskURL = import.meta.env.VITE_FLASK_URL;
    const response = await fetch(`${flaskURL}/${endpoint}`);

    if (!response.ok) {
        const errorText = await response.text(); 
        throw new Error(`Failed to fetch from Flask API: ${response.status} - ${errorText}`);
    }

    return response.json();
}


//POST
export async function sendToFlask(endpoint: string, data: object) {
    const flaskURL = import.meta.env.VITE_FLASK_URL;

    const response = await fetch(`${flaskURL}/${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const errorText = await response.text(); 
        throw new Error(`Failed to fetch from Flask API: ${response.status} - ${errorText}`);
    }

    return response.json(); 
}