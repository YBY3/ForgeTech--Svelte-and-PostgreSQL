import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { PastOrderType } from '$lib/types/OrderTypes';


export const load = async ({ locals, fetch }) => {
  let unclaimedOrders: PastOrderType[] = [];
  let claimedOrders: PastOrderType[] = [];
  let error: string | undefined = undefined;

  //Checks if User is Logged In
  if (!locals.user) {throw redirect(302, '/auth/login');}

  //Checks if User is a "employee" or "admin"
  else if (locals.user.user_type == "employee" || locals.user.user_type == "admin") {

    // Fetch unclaimed orders
    try {
      const res = await fetch(`${getFlaskURL()}/api/ordersControl/unclaimed`, {
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
      const res = await fetch(`${getFlaskURL()}/api/ordersControl/employeeDashboard/${locals.user.id}`, {
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

  }
  else {
    throw redirect(302, '/')
  }
};


export const actions = {

  claimOrder: async ({ request, fetch }) => {
    try {
      const formData = await request.formData();
      const jsonData = {
          order_id: formData.get('order_id'),
          employee_id: formData.get('employee_id')
      };

      const flaskResponse = await fetch(`${getFlaskURL()}/api/ordersControl/claim`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData)
      });

      const responseData = await flaskResponse.json();

      if (!flaskResponse.ok) {
        console.error('Claiming Order Failed:', responseData.error );
        return fail(flaskResponse.status, responseData);
      }

      return { success: true, message: responseData.message };
    } 

    catch (error) {
      console.error('Error in claimOrder action:', error);
      return fail(500, { error: 'Internal Server Error' });
    }
  },

  unclaimOrder: async ({ request, fetch }) => {
    try {
      const formData = await request.formData();
      const jsonData = {
          order_id: formData.get('order_id')
      };

      const flaskResponse = await fetch(`${getFlaskURL()}/api/ordersControl/unclaim`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData)
      });

      const responseData = await flaskResponse.json();

      if (!flaskResponse.ok) {
        console.error('Unclaiming Order Failed:', responseData.error );
        return fail(flaskResponse.status, responseData);
      }

      return { success: true, message: responseData.message };
    } 

    catch (error) {
      console.error('Error in unclaimOrder action:', error);
      return fail(500, { error: 'Internal Server Error' });
    }
  }
};