import { redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { PastOrderType } from '$lib/types/OrderTypes';
import type { UserType } from '$lib/types/UserTypes';

export const load = async ({ locals, fetch }) => {
  // Redirect if the user is not logged in
  if (!locals.user) {
    throw redirect(302, '/auth/login');
  }

  // Check if the user is an employee
  if (locals.user.user_type === 'employee') {
    let claimedOrders: PastOrderType[] = [];

    // Fetch claimed orders for the employee
    try {
      const claimedEndpoint = `${getFlaskURL()}/api/ordersControl/employeeDashboard/${locals.user.id}`;
      console.log("Requesting claimed orders from:", claimedEndpoint);
      const claimedRes = await fetch(claimedEndpoint, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      console.log("Claimed orders response status:", claimedRes.status);
      const claimedData = await claimedRes.json();
      console.log("Claimed orders data received:", claimedData);
      
      if (claimedRes.ok) {
        claimedOrders = claimedData.orders as PastOrderType[];
      } else {
        console.error("Error fetching claimed orders:", claimedData.error);
      }
    } catch (error) {
      console.error("Failed to load claimed orders:", error);
    }

    return { user: locals.user, claimedOrders };

  } else {
    // For non-employee users, fetch their past orders
    try {
      const res = await fetch(`${getFlaskURL()}/api/orders/get_all_orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: locals.user.id })
      });
      console.log("Fetch status:", res.status);
      const data = await res.json();
      console.log("Data received:", data);
      
      if (!res.ok) {
        return { user: locals.user, error: data.error || 'Failed to load past orders', pastOrders: [] };
      }
      return { user: locals.user, pastOrders: data.orders as PastOrderType[] };
    } catch (error) {
      console.error("Failed to load orders:", error);
      return { user: locals.user, error: 'Could not load orders', pastOrders: [] };
    }
  }
};

