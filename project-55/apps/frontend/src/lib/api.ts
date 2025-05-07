export function getFlaskURL() {
    const flaskURL = import.meta.env.VITE_FLASK_URL;
    return flaskURL
}

export function getImageURL() {
    const imageURL = import.meta.env.VITE_IMAGE_URL;
    return imageURL
}