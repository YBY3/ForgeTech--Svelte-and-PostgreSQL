import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';


export const load = async ({ locals }) => {
    if (locals.user) {
        return { user: locals.user };
    }
    else {
        throw redirect(302, '/auth/login');
    }
};


export const actions = {
    add_order: async ({ locals, request }) => {
        if (locals.user) {
            try {
                const formData = await request.formData();
                const productIdsString = formData.get('product_ids');
                let product_ids;
                if (typeof productIdsString === 'string') {
                    product_ids = JSON.parse(productIdsString);
                }
                else {
                    console.error('Confirming Order Failed:', "Could Not Get Product Ids" );
                    return fail(400, {error: "Could Not Get Product Ids"});
                }
                const jsonData = {
                    user_id: locals.user.id,
                    product_ids: product_ids,
                    total: formData.get('total'),
                    status: 'pending'
                };

                const flaskResponse = await fetch(`${getFlaskURL()}/api/orders/add_order`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(jsonData)
                });

                const responseData = await flaskResponse.json();

                if (!flaskResponse.ok) {
                    console.error('Confirming Order Failed:', responseData.error );
                    return fail(flaskResponse.status, responseData);
                }

                return { success: true, message: responseData.message };

            } catch (error) {
                console.error('Error in order confirmation action:', error);
                return fail(500, { error: 'Internal server error' });
            }
        }

        else {
            return fail(401, { error: 'User not authenticated' });
        }
    }
};