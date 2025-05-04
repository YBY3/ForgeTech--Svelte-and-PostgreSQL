import { redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { PastOrderType } from '$lib/types/OrderTypes';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, fetch, locals }) => {
  if (!locals.user) throw redirect(302, '/auth/login');

  const orderId = url.searchParams.get('orderId');
  if (!orderId) {
    return { user: locals.user, order: null, error: 'No order ID provided' };
  }

  let order: PastOrderType | null = null;
  let error: string | undefined;

  try {
    // NOTE: this is the customer endpoint
    const apiUrl = `${getFlaskURL()}/api/orders/orderDetails/${orderId}`;
    console.log('[server] fetching customer orderDetails →', apiUrl);
    const res = await fetch(apiUrl, { headers: { 'Content-Type': 'application/json' } });
    const data = await res.json();
    console.log('[server] customer fetch result:', data);

    if (res.ok && data.success) {
      order = data.order as PastOrderType;
      // if you want to guard ownership:
      if (order.user_id !== locals.user.id) {
        throw redirect(302, '/dashboard');
      }
    } else {
      error = data.error || 'Failed to load order details';
    }
  } catch (err) {
    console.error('Error fetching customer order details:', err);
    error = 'Could not load order details';
  }

  return { user: locals.user, order, error };
};
