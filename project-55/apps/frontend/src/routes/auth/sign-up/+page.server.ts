import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';


export const actions = {
    signup: async ({ request, cookies }) => {
        try {
            const formData = await request.formData();
            const jsonData = {
                name: `${formData.get('firstName')} ${formData.get('lastName')}`,
                username: formData.get('userName'),
                email: formData.get('email'),
                password: formData.get('password')
            };
            const flaskResponse = await fetch(`${getFlaskURL()}/api/users/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Sign-up Failed:', responseData.error );
                return fail(flaskResponse.status, responseData);
            }

            cookies.set('user', JSON.stringify(responseData.user), {
                path: '/',
                httpOnly: false,
                secure: false,
                sameSite: 'strict',
                maxAge: 1800 // 30 minutes
            });

            return { success: true };

        } catch (error) {
            console.error('Error in signup action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    }
};