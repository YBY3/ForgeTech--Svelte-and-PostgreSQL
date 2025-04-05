import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';


export const load = async ({ locals }) => {
    if (!locals.user || locals.user.user_type !== 'admin') {
        throw redirect(302, '/'); 
    }
}


export const actions = {
    createUser: async ({ request }) => {
        try {
            const formData = await request.formData();
            const jsonData = {
                name: `${formData.get('firstName')} ${formData.get('lastName')}`,
                username: formData.get('userName'),
                email: formData.get('email'),
                password: formData.get('password'),
                usertype: formData.get('usertype')
            };
            const flaskResponse = await fetch(`${getFlaskURL()}/api/users/createUser`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Sign-up Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                }
                return fail(flaskResponse.status, responseData);
            }

            return { success: true };

        } catch (error) {
            console.error('Error in signup action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    }
};