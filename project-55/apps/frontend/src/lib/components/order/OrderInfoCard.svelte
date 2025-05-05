<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import ProductSmallPreview from '$lib/components/product/ProductSmallPreview.svelte';
	import type { OrderType } from '$lib/types/OrderTypes';
	import type { ProductOrderPreviewType } from '$lib/types/ProductTypes';

	export let order: OrderType;
	export let showCancelButton = false;
	export let showClaimButton  = false;
	const dispatch = createEventDispatcher();

	// 1) Derive a grouped list: sum quantities by product.id
	$: groupedProducts = (() => {
		const map = new Map<number, ProductOrderPreviewType>();
		for (const p of order.products) {
			const existing = map.get(p.id);
			if (existing) {
				existing.quantity += p.quantity;
			} else {
				// clone so we don't mutate original
				map.set(p.id, { ...p });
			}
		}
		return Array.from(map.values());
	})();

	function handleCancelButtonClick(orderID: number) {
		dispatch('cancelRequest', { orderID });
	}

	function handleClaimButtonClick(orderID: number, orderStatus: string) {
		dispatch('claimRequest', { orderID, orderStatus });
	}
</script>

{#if order}
	<div class="w-full flex flex-col items-center gap-2 card variant-surface p-3">
		<strong>Created: {new Date(order.created_at).toLocaleString()}</strong>
		<div class="w-full flex flex-col items-start text-center rounded-lg gap-1 p-2">
			<div>Order Info:</div>
			<div>Total: ${order.total}</div>
			<div>Status: {order.status}</div>
		</div>

		<div class="w-full p-2 rounded-lg">
			{#if groupedProducts.length > 0}
				{#each groupedProducts as product (product.id)}
					<div class="w-full flex gap-3 items-center pl-3 pr-3 py-2">
						<ProductSmallPreview {product} />
						<!-- <span class="font-semibold">x{product.quantity}</span> -->
					</div>
				{/each}
			{:else}
				<div class="w-full text-center p-4">
					No Products Found
				</div>
			{/if}
		</div>

		{#if showCancelButton}
			<button 
				class="w-1/2 btn variant-filled-primary text-lg p-2 rounded-lg"
				on:click={() => handleCancelButtonClick(order.id)}
			>
				Cancel Order
			</button>
		{/if}

		{#if showClaimButton}
			<button 
				class="w-1/2 btn variant-filled-primary text-lg p-2 rounded-lg"
				on:click={() => handleClaimButtonClick(order.id, order.status)}
			>
				{order.status === 'pending' ? 'Claim Order' : 'Unclaim Order'}
			</button>
		{/if}
	</div>
{/if}
