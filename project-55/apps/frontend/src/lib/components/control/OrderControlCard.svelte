<script lang="ts">
	import ProductSmallPreview from '$lib/components/product/ProductSmallPreview.svelte';
	import type { PastOrderType } from '$lib/types/OrderTypes';
	import type { ProductOrderPreviewType } from '$lib/types/ProductTypes';
  
	export let order: PastOrderType;
  
	// group duplicates
	$: groupedProducts = (() => {
	  const map = new Map<number, ProductOrderPreviewType>();
	  for (const p of order.products) {
		const existing = map.get(p.id);
		if (existing) {
		  existing.quantity += p.quantity;
		} else {
		  map.set(p.id, { ...p });
		}
	  }
	  return Array.from(map.values());
	})();
  </script>
  
  <article class="card variant-surface p-4 flex flex-col gap-4">
	<!-- Order ID, Status and Time Placed all in one flex-col -->
	<div class="flex flex-col space-y-1">
	  <div><strong>Order ID:</strong> {order.id}</div>
	  <div><strong>Status:</strong> {order.status}</div>
	  <div>
		<strong>Time Placed:</strong>
		{new Date(order.created_at).toLocaleString()}
	  </div>
	</div>
  
	<!-- Products still get the gap-4 from the parent -->
	<div>
	  <strong>Products:</strong>
	  <div class="mt-2 space-y-2">
		{#each groupedProducts as product (product.id)}
		  <ProductSmallPreview
			product={product}
			showOverlay={false}
		  />
		{/each}
	  </div>
	</div>
  </article>
  
  
  