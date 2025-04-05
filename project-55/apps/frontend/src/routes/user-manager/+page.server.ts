import { redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { UserType } from '$lib/types/UserTypes.js';


export const load = async ({ locals, fetch }) => {

    if (!locals.user || locals.user.user_type !== 'customer') {
        throw redirect(302, '/auth/login'); 
    }

    try {
        const response = await fetch(`${getFlaskURL()}/api/users/get_users`);

        if (!response.ok) {
            throw new Error('Failed to fetch users');
        }
        const users: UserType[] = await response.json();
        
        return {
            user: locals.user ?? null,
            users: users 
        };
    } 
    
    catch (error) {
        console.error('Error fetching users:', error);
        return { user: locals.user ?? null, users: [] };
    }
};


export const actions = {
    deleteUser: async ({ request }) => {
        try {
            const formData = await request.formData();
            const jsonData = { id: formData.get('id') }

            if (!jsonData) {
                return { error: "User ID is required" };
            }

            const response = await fetch(`${getFlaskURL()}/api/users/deleteUser`, {  
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(jsonData)
            });

            if (!response.ok) {
                throw new Error('Failed to delete user');
            }

            return { success: true };
        } catch (error) {
            console.error("Error deleting user:", error);
            return { error: "joe mama" };
        }
    }
};
