<script lang="ts">
	import { getFlaskURL } from '$lib/api';
	export let data;
	const { user, order, error } = data;
  
	async function confirmOrder() {
		if (!order) return;
			try {
				const res = await fetch(`${getFlaskURL()}/api/ordersControl/confirm`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					order_id: order.id,
					employee_id: user.id
				})
				});
				if (!res.ok) {
				console.error('Error confirming order:', await res.json());
				} else {
				const updatedOrder = await res.json();
				console.log('Order confirmed:', updatedOrder);
				// Force a full page reload
				location.reload();
				}
			} catch (err) {
				console.error('Error in confirmOrder:', err);
		}
	}

	async function workingOrder() {
	if (!order) return;
		try {
			const res = await fetch(`${getFlaskURL()}/api/ordersControl/working`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				order_id: order.id,
				employee_id: user.id
			})
			});
			if (!res.ok) {
			console.error('Error marking order as working:', await res.json());
			} else {
			const updatedOrder = await res.json();
			console.log('Order marked as working:', updatedOrder);
			// Force a full page reload
			location.reload();
			}
		} catch (err) {
			console.error('Error in workingOrder:', err);
		}
	}

	async function removeOrder() {
	if (!order) return;
		try {
			const res = await fetch(`${getFlaskURL()}/api/ordersControl/unclaim`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				order_id: order.id
			})
			});
			if (!res.ok) {
			console.error('Error unclaiming order:', await res.json());
			} else {
			const updatedOrder = await res.json();
			console.log('Order unclaimed:', updatedOrder);
			// Force a full page reload
			location.reload();
			}
		} catch (err) {
			console.error('Error in removeOrder:', err);
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
			  {product.name} - ${product.price}
			</li>
		  {/each}
		</ul>
		<!-- Action Buttons Row -->
		<div class="flex flex-wrap justify-around mt-6 gap-4">
		  <button on:click={removeOrder} class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition">
			Unclaim Order
		  </button>
		  <button on:click={workingOrder} class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition">
			Working
		  </button>
		  <button on:click={confirmOrder} class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition">
			Confirm
		  </button>
		</div>
		<!-- Back to Profile Button Row -->
		<div class="flex justify-center mt-4">
		  <a href="/profile" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
			Back to Profile
		  </a>
		</div>
	  </div>
	{:else}
	  <p class="text-center text-gray-500">Loading order details...</p>
	{/if}
</div>
