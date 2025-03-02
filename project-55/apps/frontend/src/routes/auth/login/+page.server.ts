import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import { invalidate } from '$app/navigation';


export const actions = {
    login: async ({ request, cookies }) => {
        try {
            const formData = await request.formData();
            const jsonData = {
                email: formData.get('email'),
                password: formData.get('password')
            };

            const flaskResponse = await fetch(`${getFlaskURL()}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok || !responseData.success) {
                return fail(flaskResponse.status, { message: responseData.error || 'Login failed' });
            }

            cookies.set('user', JSON.stringify(responseData.user), {
                path: '/',
                httpOnly: false,
                secure: false,   
                sameSite: 'strict',
                maxAge: 1800 // 30 minutes in seconds
            });

            invalidate('app:load');
            return { success: true };
        } 
        
        catch (error) {
            console.error('Error in login action:', error);
            return fail(500, { message: 'Internal server error' });
        }
    }
};