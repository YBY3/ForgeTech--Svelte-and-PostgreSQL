import { redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { PastOrderType } from '$lib/types/OrderTypes';
import type { UserType } from '$lib/types/UserTypes';

export const load = async ({ locals, fetch }) => {
  // Only allow employee users
  if (!locals.user || locals.user.user_type !== 'employee') {
    throw redirect(302, '/auth/login');
  }

  let unclaimedOrders: PastOrderType[] = [];
  let claimedOrders: PastOrderType[] = [];
  let error: string | undefined = undefined;

  // Fetch unclaimed orders
  try {
    const res = await fetch(`${getFlaskURL()}/api/orders/unclaimed`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    console.log("Unclaimed orders response status:", res.status);
    const data = await res.json();
    console.log("Unclaimed orders data received:", data);
    if (res.ok) {
      unclaimedOrders = data.orders as PastOrderType[];
    } else {
      console.error("Error fetching unclaimed orders:", data.error);
      error = data.error || 'Failed to load unclaimed orders';
    }
  } catch (err) {
    console.error("Failed to load unclaimed orders:", err);
    error = 'Could not load unclaimed orders';
  }

  // Fetch claimed orders for the employee dashboard
  try {
    const res = await fetch(`${getFlaskURL()}/api/orders/employeeDashboard/${locals.user.id}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    console.log("Claimed orders response status:", res.status);
    const data = await res.json();
    console.log("Claimed orders data received:", data);
    if (res.ok) {
      claimedOrders = data.orders as PastOrderType[];
    } else {
      console.error("Error fetching claimed orders:", data.error);
      error = data.error || 'Failed to load claimed orders';
    }
  } catch (err) {
    console.error("Failed to load claimed orders:", err);
    error = 'Could not load claimed orders';
  }

  return { user: locals.user, unclaimedOrders, claimedOrders, error };
};

