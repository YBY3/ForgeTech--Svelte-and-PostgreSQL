<script lang="ts">
	import { getFlaskURL } from '$lib/api';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import type { PastOrderType } from '$lib/types/OrderTypes';
	import type { UserType } from '$lib/types/UserTypes';
	// Data loaded from the TS load function
	export let data: {
	  user: UserType;
	  order: PastOrderType;
	  error?: string;
	};
  
	// Set local variables from loaded data.
	const { user, order: initialOrder, error: initialError } = data;
	let order: PastOrderType = initialOrder;
	let error = initialError;
	let submitting = false;
	const toastStore = getToastStore();
  
	// Confirm order action – calls the TS action via the relative endpoint.
	async function confirmOrder() {
	  if (!order || submitting) return;
	  submitting = true;
	  try {
		const formData = new FormData();
		formData.append("order_id", JSON.stringify(order.id));
		formData.append("employee_id", JSON.stringify(user.id));
  
		// Call the relative endpoint that maps to the TS action.
		const response = await fetch('?/confirmOrder', {
		  method: 'POST',
		  body: formData
		});
		const result = await response.json();
		// Our order‑control code does an extra JSON.parse on result.data
		const parsedResultData = JSON.parse(result.data);
		const success = parsedResultData[parsedResultData[0].success];
		if (success) {
		  // Option 1: Use the success message coming from the API...
		  const successMessage = parsedResultData[parsedResultData[0].message] || 'Order confirmed successfully';
		  // Trigger the success toast.
		  toastStore.trigger({
			message: successMessage,
			background: 'variant-filled-success'
		  });
		  // Option 2: If you want an extra static confirmation, uncomment below:
		  // toastStore.trigger({ message: 'Order confirmed successfully', background: 'variant-filled-success' });
		  
		  // Update local order – mimic what the backend does (status becomes confirmed)
		  order = { ...order, status: "confirmed" };
		} else {
		  const errorMessage = parsedResultData[parsedResultData[0].error];
		  throw new Error(errorMessage);
		}
	  } catch (error) {
		const errorMessage: string = `${error}`;
		toastStore.trigger({
		  message: errorMessage,
		  background: 'variant-filled-error'
		});
	  } finally {
		submitting = false;
	  }
	}
  
	// Working order action.
	async function workingOrder() {
	  if (!order || submitting) return;
	  submitting = true;
	  try {
		const formData = new FormData();
		formData.append("order_id", JSON.stringify(order.id));
		formData.append("employee_id", JSON.stringify(user.id));
  
		const response = await fetch('?/workingOrder', {
		  method: 'POST',
		  body: formData
		});
		const result = await response.json();
		const parsedResultData = JSON.parse(result.data);
		const success = parsedResultData[parsedResultData[0].success];
		if (success) {
		  const successMessage = parsedResultData[parsedResultData[0].message] || 'Order marked as working';
		  toastStore.trigger({
			message: successMessage,
			background: 'variant-filled-success'
		  });
		  // Update order status to working.
		  order = { ...order, status: "working" };
		} else {
		  const errorMessage = parsedResultData[parsedResultData[0].error];
		  throw new Error(errorMessage);
		}
	  } catch (error) {
		const errorMessage: string = `${error}`;
		toastStore.trigger({
		  message: errorMessage,
		  background: 'variant-filled-error'
		});
	  } finally {
		submitting = false;
	  }
	}
  
	// Unclaim order action.
	async function unclaimOrder() {
	  if (!order || submitting) return;
	  submitting = true;
	  try {
		const formData = new FormData();
		formData.append("order_id", JSON.stringify(order.id));
		
		const response = await fetch('?/unclaimOrder', {
		  method: 'POST',
		  body: formData
		});
		const result = await response.json();
		const parsedResultData = JSON.parse(result.data);
		const success = parsedResultData[parsedResultData[0].success];
		if (success) {
		  const successMessage = parsedResultData[parsedResultData[0].message] || 'Order unclaimed successfully';
		  toastStore.trigger({
			message: successMessage,
			background: 'variant-filled-success'
		  });
		  // Update local order to reflect unclaimed status.
		  order = { ...order, status: "pending", claimed_by_employee_id: undefined };
		} else {
		  const errorMessage = parsedResultData[parsedResultData[0].error];
		  throw new Error(errorMessage);
		}
	  } catch (error) {
		const errorMessage: string = `${error}`;
		toastStore.trigger({
		  message: errorMessage,
		  background: 'variant-filled-error'
		});
	  } finally {
		submitting = false;
	  }
	}
</script>
  
<div class="max-w-5xl mx-auto p-6">
	{#if error}
	  <p class="text-center text-red-500 text-xl font-semibold">{error}</p>
	{:else if order}
	  <div class="border rounded-lg p-4 shadow hover:shadow-lg transition">
		<h1 class="text-center text-4xl font-bold mb-4">Order Detail: #{order.id}</h1>
		<p class="mb-2"><strong>Total:</strong> ${order.total.toFixed(2)}</p>
		<p class="mb-2"><strong>Status:</strong> {order.status}</p>
		<p class="mb-2">
		  <strong>Time Placed:</strong> {new Date(order.created_at).toLocaleString()}
		</p>
		<h2 class="text-2xl font-semibold mt-4 mb-2">Products:</h2>
		<ul class="space-y-2 mb-4">
		  {#each order.products as product}
			<li class="p-2 border rounded">
			  {product.name} - ${product.price} <span class="font-semibold">x{product.quantity}</span>
			</li>
		  {/each}
		</ul>
		<!-- Action Buttons Row -->
		<div class="flex flex-wrap justify-around mt-6 gap-4">
		  <button on:click|stopPropagation={unclaimOrder} disabled={submitting}
			class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition">
			Unclaim Order
		  </button>
		  <button on:click|stopPropagation={workingOrder} disabled={submitting}
			class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition">
			Working
		  </button>
		  <button on:click|stopPropagation={confirmOrder} disabled={submitting}
			class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition">
			Confirm
		  </button>
		</div>
		<div class="flex justify-center mt-4">
		  <a href="/auth/order-control" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
			Back to Order Control
		  </a>
		</div>
	  </div>
	{:else}
	  <p class="text-center text-gray-500">Loading order details...</p>
	{/if}
</div>

