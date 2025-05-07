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
		<!-- Outer card -->
		<div class="card variant-surface p-6 space-y-6 shadow-sm hover:shadow-md transition">
			<!-- Title -->
			<h1 class="text-center text-4xl font-bold">Order Detail: #{order.id}</h1>

			<!-- Summary metrics -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<div class="card variant-ghost p-4 text-center">
					<p class="text-sm font-medium text-gray-500">Total</p>
					<p class="mt-1 text-xl font-semibold">${order.total.toFixed(2)}</p>
				</div>
				<div class="card variant-ghost p-4 text-center">
					<p class="text-sm font-medium text-gray-500">Status</p>
					<p class="mt-1 text-xl font-semibold capitalize">{order.status}</p>
				</div>
				<div class="card variant-ghost p-4 text-center">
					<p class="text-sm font-medium text-gray-500">Time Placed</p>
					<p class="mt-1 text-xl font-semibold">
						{new Date(order.created_at).toLocaleString()}
					</p>
				</div>
			</div>

			<!-- Products list header -->
			<h2 class="text-2xl font-semibold">Products</h2>

			<!-- Products list -->
			<ul class="space-y-4">
				{#each order.products as product}
					<li
						class="card variant-ghost p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4"
					>
						<div>
							<p class="font-semibold text-lg">{product.name}</p>
							{#if product.product_option}
								<p class="mt-1 text-sm text-gray-600">
									Option: {product.product_option}
								</p>
							{/if}
						</div>
						<div class="flex items-center gap-6 text-sm">
							<span class="font-medium">Qty: {product.quantity}</span>
							<span class="font-medium">Price: ${product.price.toFixed(2)}</span>
						</div>
					</li>
				{/each}
			</ul>

			<!-- Action buttons (all blank/ghost now) -->
				<div class="flex flex-wrap justify-center gap-4">
					<button
					on:click|stopPropagation={unclaimOrder}
					disabled={submitting}
					class="btn variant-ghost px-6 py-2"
					>
					Unclaim
					</button>
				
					<button
					on:click|stopPropagation={workingOrder}
					disabled={submitting}
					class="btn variant-ghost px-6 py-2"
					>
					Working
					</button>
				
					<button
					on:click|stopPropagation={confirmOrder}
					disabled={submitting}
					class="btn variant-ghost px-6 py-2"
					>
					Confirm
					</button>
				</div>

			<!-- Back link -->
			<div class="flex justify-center mt-4">
				<a
					href="/control/order-control"
					class="btn variant-filled-primary px-6 py-2"
				>
					Back to Order Control
				</a>
			</div>
		</div>
	{:else}
		<p class="text-center text-gray-500">Loading order details...</p>
	{/if}
</div>

