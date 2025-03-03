import { redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { PastOrderType } from '$lib/types/OrderTypes.js';


export const load = async ({ locals, fetch }) => { //this one is subject to change
    if (locals.user) {

        try {
            const flaskResponse = await fetch(`${getFlaskURL()}/api/orders/get_all_orders`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: locals.user.id })
            });
    
            const reponseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                return { user: locals.user, error: reponseData.error || 'Failed to Fetch Past Orders' };
            }
            
            const pastOrders: PastOrderType[] = reponseData.orders;

            return { 
                user: locals.user, 
                pastOrders: pastOrders
            };
        } 

        catch (error) {
            console.error("Failed to Load User's Past Orders: ", error);
            return { user: locals.user, error: 'Could Not Load Past Orders' };
        }
    }
    else {
        throw redirect(302, '/auth/login');
    }
};