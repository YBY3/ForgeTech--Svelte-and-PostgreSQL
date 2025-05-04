import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';

export const load = async ({ locals }) => {
	if (locals.user) {
		return { user: locals.user };
	}
	throw redirect(302, '/auth/login');
};

export const actions = {
	add_order: async ({ locals, request }) => {
		if (!locals.user) {
			return fail(401, { error: 'User not authenticated' });
		}

		try {
			const form = await request.formData();

			// 1) product_ids
			const idsRaw = form.get('product_ids');
			if (typeof idsRaw !== 'string') {
				return fail(400, { error: 'Missing product_ids' });
			}
			const product_ids: number[] = JSON.parse(idsRaw);

			// 2) product_options
			const optsRaw = form.get('product_options');
			if (typeof optsRaw !== 'string') {
				return fail(400, { error: 'Missing product_options' });
			}
			const product_options: string[] = JSON.parse(optsRaw);

			if (product_ids.length !== product_options.length) {
				return fail(400, { error: 'Mismatched IDs/options lengths' });
			}

			// 3) total
			const totalRaw = form.get('total');
			if (typeof totalRaw !== 'string') {
				return fail(400, { error: 'Missing total' });
			}

			// 4) assemble payload
			const jsonData = {
				user_id:          locals.user.id,
				product_ids,
				product_options,
				total:            totalRaw,
				status:           'pending'
			};

			console.log('Action add_order payload →', JSON.stringify(jsonData, null, 2));

			// 5) forward to Flask
			const resp = await fetch(`${getFlaskURL()}/api/orders/add_order`, {
				method:  'POST',
				headers: { 'Content-Type': 'application/json' },
				body:    JSON.stringify(jsonData)
			});

			const data = await resp.json();
			console.log('Flask response:', data);

			if (!resp.ok) {
				return fail(resp.status, data);
			}

			return { success: true, message: data.message };
		} catch (e) {
			console.error('Error in order confirmation action:', e);
			return fail(500, { error: 'Internal server error' });
		}
	}
};
