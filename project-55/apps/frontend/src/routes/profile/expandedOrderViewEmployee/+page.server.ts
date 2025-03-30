// routes/expandedOrderViewEmployee/+page.server.ts
import { redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { PastOrderType } from '$lib/types/OrderTypes';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, fetch, locals }) => {
  // Debug: Log local user details
  console.log("locals.user:", locals.user);

  // Only allow employee users
  if (!locals.user || locals.user.user_type !== 'employee') {
    console.error("Access denied: User not authenticated or not an employee");
    throw redirect(302, '/auth/login');
  }

  // Get the order ID from query parameters
  const orderId = url.searchParams.get('orderId');
  console.log("Received orderId from query parameters:", orderId);
  
  if (!orderId) {
    console.error("No order ID provided in query parameters");
    return { error: 'No order ID provided' };
  }

  let order: PastOrderType | null = null;
  let error: string | undefined = undefined;

  try {
    const apiUrl = `${getFlaskURL()}/api/ordersControl/orderDetails/${orderId}`;
    console.log("Fetching order details from:", apiUrl);

    const res = await fetch(apiUrl, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    console.log("Response status:", res.status);

    const data = await res.json();
    console.log("Response data:", data);

    if (res.ok && data.success) {
      order = data.order as PastOrderType;
      console.log("Order retrieved successfully:", order);
    } else {
      error = data.error || 'Failed to load order details';
      console.error("Error fetching order details:", error);
    }
  } catch (err) {
    error = 'Could not load order details';
    console.error("Exception while fetching order details:", err);
  }

  return { user: locals.user, order, error };
};
