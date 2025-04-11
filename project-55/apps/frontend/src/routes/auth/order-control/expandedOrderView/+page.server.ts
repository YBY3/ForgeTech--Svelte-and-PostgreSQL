// routes/expandedOrderViewEmployee/+page.server.ts
import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { PastOrderType } from '$lib/types/OrderTypes';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ url, fetch, locals }) => {
  // Only allow employee users.
  if (!locals.user || locals.user.user_type !== 'employee') {
    throw redirect(302, '/auth/login');
  }

  // Get the order ID from query parameters.
  const orderId = url.searchParams.get('orderId');
  if (!orderId) {
    return { error: 'No order ID provided' };
  }

  let order: PastOrderType | null = null;
  let error: string | undefined = undefined;

  try {
    const apiUrl = `${getFlaskURL()}/api/ordersControl/orderDetails/${orderId}`;
    const res = await fetch(apiUrl, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    if (res.ok && data.success) {
      order = data.order as PastOrderType;
    } else {
      error = data.error || 'Failed to load order details';
    }
  } catch (err) {
    error = 'Could not load order details';
    console.error("Error fetching order details:", err);
  }

  return { user: locals.user, order, error };
};

export const actions: Actions = {
  confirmOrder: async ({ request, fetch }) => {
    try {
      const formData = await request.formData();
      const jsonData = {
        order_id: formData.get('order_id'),
        employee_id: formData.get('employee_id')
      };

      const flaskResponse = await fetch(`${getFlaskURL()}/api/ordersControl/confirm`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData)
      });

      const responseData = await flaskResponse.json();

      if (!flaskResponse.ok) {
        console.error('Confirming Order Failed:', responseData.error);
        return fail(flaskResponse.status, responseData);
      }

      // Return response as a JSON string in the data property.
      return { success: true, message: responseData.message, data: JSON.stringify(responseData) };
    } catch (error) {
      console.error('Error in confirmOrder action:', error);
      return fail(500, { error: 'Internal Server Error' });
    }
  },

  workingOrder: async ({ request, fetch }) => {
    try {
      const formData = await request.formData();
      const jsonData = {
        order_id: formData.get('order_id'),
        employee_id: formData.get('employee_id')
      };

      const flaskResponse = await fetch(`${getFlaskURL()}/api/ordersControl/working`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData)
      });

      const responseData = await flaskResponse.json();

      if (!flaskResponse.ok) {
        console.error('Marking Order as Working Failed:', responseData.error);
        return fail(flaskResponse.status, responseData);
      }

      return { success: true, message: responseData.message, data: JSON.stringify(responseData) };
    } catch (error) {
      console.error('Error in workingOrder action:', error);
      return fail(500, { error: 'Internal Server Error' });
    }
  },

  unclaimOrder: async ({ request, fetch }) => {
    try {
      const formData = await request.formData();
      const jsonData = { order_id: formData.get('order_id') };

      const flaskResponse = await fetch(`${getFlaskURL()}/api/ordersControl/unclaim`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData)
      });
      const responseData = await flaskResponse.json();

      if (!flaskResponse.ok) {
        console.error('Unclaiming Order Failed:', responseData.error);
        return fail(flaskResponse.status, responseData);
      }

      return { success: true, message: responseData.message, data: JSON.stringify(responseData) };
    } catch (error) {
      console.error('Error in unclaimOrder action:', error);
      return fail(500, { error: 'Internal Server Error' });
    }
  }
};
