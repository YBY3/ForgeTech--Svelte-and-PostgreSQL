import { redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { PastOrderType } from '$lib/types/OrderTypes.js';

// This is the original incase the updated one doesn't work

// export const load = async ({ locals, fetch }) => { //this one is subject to change
//     if (locals.user) {

//         try {
//             const flaskResponse = await fetch(`${getFlaskURL()}/api/orders/get_all_orders`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ user_id: locals.user.id })
//             });
    
//             const reponseData = await flaskResponse.json();

//             if (!flaskResponse.ok) {
//                 return { user: locals.user, error: reponseData.error || 'Failed to Fetch Past Orders' };
//             }
            
//             const pastOrders: PastOrderType[] = reponseData.orders;

//             return { 
//                 user: locals.user, 
//                 pastOrders: pastOrders
//             };
//         } 

//         catch (error) {
//             console.error("Failed to Load User's Past Orders: ", error);
//             return { user: locals.user, error: 'Could Not Load Past Orders' };
//         }
//     }
//     else {
//         throw redirect(302, '/auth/login');
//     }
// };




// Tried to update this to fit userType conditional 
export const load = async ({ locals, fetch }) => {
    if (locals.user) {
        try {

            // Check if the user is an employee or a customer using the existing user_type field
            if (locals.user.user_type === 'employee') {
                // Fetch all orders claimed by the employee (still treated as PastOrderType)
                const flaskResponse = await fetch(`${getFlaskURL()}/api/employee/${locals.user.id}/dashboard`, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' }
                });

                if (!flaskResponse.ok) {
                    return { user: locals.user, error: 'Failed to Fetch Claimed Orders' };
                }

                const responseData = await flaskResponse.json();
                const pastOrders: PastOrderType[] = responseData.orders.map((order: any) => ({
                    ...order,
                    status: 'Claimed' // You can add more logic to handle specific employee statuses if needed
                })) as PastOrderType[];

            } else {
                // Fetch past orders for customers
                const flaskResponse = await fetch(`${getFlaskURL()}/api/orders/get_all_orders`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: locals.user.id })
                });

                if (!flaskResponse.ok) {
                    return { user: locals.user, error: 'Failed to Fetch Past Orders' };
                }

                const responseData = await flaskResponse.json();
                const pastOrders: PastOrderType[] = responseData.orders;
            
                return {
                    user: locals.user, 
                    pastOrders: pastOrders
                };
            }

        } catch (error) {
            console.error("Failed to Load Orders: ", error);
            return { user: locals.user, error: 'Could Not Load Orders' };
        }
    } else {
        throw redirect(302, '/auth/login');
    }
};
