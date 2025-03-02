export function getFlaskURL() {
    const flaskURL = import.meta.env.VITE_FLASK_URL;
    return flaskURL
}