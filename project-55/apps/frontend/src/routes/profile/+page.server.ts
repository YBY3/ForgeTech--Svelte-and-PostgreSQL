import { redirect } from '@sveltejs/kit';


export const load = async ({ locals }) => {
    if (locals.user) {
        return { user: locals.user };
    }
    else {
        throw redirect(302, '/auth/login');
    }
};