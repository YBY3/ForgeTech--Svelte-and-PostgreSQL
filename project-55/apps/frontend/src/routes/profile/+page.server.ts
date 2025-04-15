import { redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { PastOrderType } from '$lib/types/OrderTypes';

export const load = async ({ locals, fetch }) => {
  // Redirect if the user is not logged in
  if (!locals.user) {
    throw redirect(302, '/auth/login');
  }
  
  if (locals.user && locals.user.user_type === 'admin') {

    let allOrders: PastOrderType[] = [];
    let allUsers: any[] = [];
    let error: string | undefined = undefined;

    // Fetch recent users
    try {
      const usersEndpoint = `${getFlaskURL()}/api/users/get_users`;
      const usersRes = await fetch(usersEndpoint, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      if (usersRes.ok) {
        allUsers = await usersRes.json();;
      }
    } catch (error) {
      console.error("Failed to load users:", error);
    }
    (locals as any).recentUsers = allUsers;

    // Fetch orders
    try {
      const res = await fetch(`${getFlaskURL()}/api/orders/getOrders`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await res.json();
      if (res.ok) {
        allOrders = data.orders as PastOrderType[];
      } else {
        error = data.error || 'Failed to load unclaimed orders';
      }
    } catch (err) {
      error = 'Could not load unclaimed orders';
    }

    //Fetch Claimed Orders 
    let claimedOrders: PastOrderType[] = [];

    // Fetch claimed orders for the employee or admin
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

    return { 
      user: locals.user, 
      recentUsers: (locals as any).recentUsers, // Attach all users here
      orders: allOrders,  // Attach all orders here
      claimedOrders: claimedOrders
    };
    
  } 
  
  if (locals.user.user_type === 'employee' || locals.user.user_type === 'admin') {

    let claimedOrders: PastOrderType[] = [];
    
    // Fetch claimed orders for the employee or admin
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
    return { user: locals.user, claimedOrders, recentUsers: (locals as any).recentUsers };
  
  
  } else {
    // For non-employee, non-admin (customers)
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
