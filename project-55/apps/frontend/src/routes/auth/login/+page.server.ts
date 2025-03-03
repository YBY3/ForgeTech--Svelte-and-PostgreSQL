import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';


export const actions = {
    login: async ({ request, cookies }) => {
        try {
            const formData = await request.formData();
            const jsonData = {
                email: formData.get('email'),
                password: formData.get('password')
            };

            const flaskResponse = await fetch(`${getFlaskURL()}/api/users/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Login Failed:', responseData.error );
                return fail(flaskResponse.status, responseData);
            }

            cookies.set('user', JSON.stringify(responseData.user), {
                path: '/',
                httpOnly: false,
                secure: false,   
                sameSite: 'strict',
                maxAge: 1800 // 30 minutes in seconds
            });

            return { success: true };
        } 
        
        catch (error) {
            console.error('Error in login action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    }
};