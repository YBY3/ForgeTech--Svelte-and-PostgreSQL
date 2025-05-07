export async function handle({ event, resolve }) {
    const userCookie = event.cookies.get('user');

    if (userCookie) {
        try {
            event.locals.user = JSON.parse(userCookie);
        } 

        catch (error) {
            console.error('Invalid user cookie:', error);
            event.locals.user = null; // Reset if cookie is corrupted
        }
    }
    
    else {
        event.locals.user = null; // No user found
    }

    return resolve(event);
}