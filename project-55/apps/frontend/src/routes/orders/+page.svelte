<script lang="ts">
	import { onMount } from 'svelte';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { ordersStore, removeFromOrder } from '$lib/stores/OrdersStore';
	import type { UserType } from '$lib/types/UserTypes.js';
	import { goto } from '$app/navigation';

	export let data: { user: UserType };
	let userData: UserType;
	const toastStore = getToastStore();
	let submitting = false;

	onMount(() => {
		if (data.user) userData = data.user;
	});

	async function placeOrder() {
		if (submitting) {
			toastStore.trigger({ message: 'Already confirming order, please wait', background: 'variant-filled-error' });
			return;
		}
		if (!$ordersStore.length) {
			toastStore.trigger({ message: 'Your cart is empty', background: 'variant-filled-error' });
			return;
		}

		// 1) Build parallel arrays of IDs & options
		const product_ids     = $ordersStore.map(item => item.id);
		const product_options = $ordersStore.map(item => item.product_option ?? 'none');

		// 2) Package into FormData
		const formData = new FormData();
		formData.append('product_ids',     JSON.stringify(product_ids));
		formData.append('product_options', JSON.stringify(product_options));
		formData.append(
			'total',
			$ordersStore
				.reduce((sum, item) => sum + item.price * (item.quantity ?? 1), 0)
				.toFixed(2)
		);
		formData.append('status', 'pending');

		// 3) Log for debugging
		for (const [key, value] of formData.entries()) {
			console.log(`Submitting formData: ${key} =`, value);
		}

		try {
			submitting = true;
			const response = await fetch('?/add_order', {
				method: 'POST',
				body:   formData
			});
			const result = await response.json();
			console.log('Backend response:', result);

			if (!response.ok) {
				throw new Error(result.error || 'Failed to confirm order');
			}

			ordersStore.set([]);
			toastStore.trigger({ message: 'Order confirmed!', background: 'variant-filled-success' });
			//goto('/orders/confirmation');
		} catch (err) {
			toastStore.trigger({ message: `${err}`, background: 'variant-filled-error' });
		} finally {
			submitting = false;
		}
	}
</script>

{#if userData}
<div class="h-full overflow-y-auto">
	<div class="max-w-5xl mx-auto p-6"> 
		<h1 class="text-3xl font-bold text-center mb-6">Shopping Cart</h1>

		{#if $ordersStore.length === 0}
			<p class="text-center text-lg">
				Your cart is empty. <a href="/catalog" class="text-blue-500">Browse Products</a>
			</p>
		{:else}
			<ul class="space-y-4">
				{#each $ordersStore as product, index (product.id + '-' + (product.product_option ?? '') + '-' + index)}
					<li class="flex items-center justify-between p-4 bg-surface-200 dark:bg-surface-700 rounded-lg shadow">
						<div class="flex items-center gap-4">
							<img
								src={product.image_urls[0]}
								alt={product.name}
								class="w-16 h-16 object-contain rounded-md bg-gray-100" />
							<div class="flex flex-col">
								<h2 class="text-lg font-semibold">{product.name}</h2>
								<p class="text-gray-600">${product.price.toFixed(2)}</p>
								{#if product.product_option}
									<p class="text-gray-600">
									Option: {product.product_option ?? 'None'}
								  </p>
								{/if}
								{#if product.quantity}
									<p class="text-gray-600">Qty: {product.quantity}</p>
								{/if}
							</div>
						</div>
						<button
							on:click={() => removeFromOrder(product.id)}
							class="text-red-500 hover:text-red-700 transition"
						>
							<i class="fa-solid fa-trash"></i>
						</button>
					</li>
				{/each}
			</ul>

			<div class="mt-6 text-center">
				<p class="text-xl font-semibold">
					Total: $
					{ $ordersStore
						.reduce((sum, item) => sum + item.price * (item.quantity ?? 1), 0)
						.toFixed(2)
					}
				</p>
			</div>

			<div class="text-center mt-4">
				<button
					on:click={placeOrder}
					disabled={!$ordersStore.length || submitting}
					class="px-8 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed"
				>
					Confirm Order
				</button>
			</div>
		{/if}
	</div>
</div>
{/if}
