import { sendToFlask } from '$lib/api';
import { fail } from '@sveltejs/kit';


export const actions = {
    signup: async ({ request }) => {

        try {
            const formData = await request.formData();

            // Convert FormData to an object matching Flask's expected JSON
            const jsonData = {
                username: `${formData.get('firstName')}${formData.get('lastName')}`,
                password: formData.get('password'),
                email: formData.get('email')
            };

            // Call sendToFlask to send the data to Flask
            const flaskResponse = await sendToFlask('signup', jsonData);

            // If Flask returns an unexpected success=false, fail gracefully
            return fail(400, { message: flaskResponse.error || 'Signup failed' });
        } catch (error) {
            console.error('Error in signup action:', error);

            if (error instanceof Response && error.status === 303) {
                throw error;
            }

            // Extract status and message from sendToFlask error
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            const statusMatch = errorMessage.match(/Failed to fetch from Flask API: (\d+)/);
            const status = statusMatch ? parseInt(statusMatch[1], 10) : 500;

            // Return failure response to the client
            return fail(status >= 200 && status < 600 ? status : 500, {
                message: errorMessage
            });
        }
    }
};