<script lang="ts">
	import ProductCard from '$lib/components/product/ProductCard.svelte';
	import type { ProductType } from '$lib/types/ProductTypes';
	import { addToOrder } from "$lib/stores/OrdersStore";
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
  
	export let isLoggedIn = false;
	export let data: {
	  user: any;
	  product: ProductType;
	  isLoggedIn: boolean;
	  productData: ProductType[];
	};
  
	let relatedProducts: ProductType[] = [];
	let currentImageIndex = 0;
  
	// --- NEW: track the chosen option ---
	let selectedOption = '';
  
	const hasOptions = data.product.options?.length > 0;
	const isInStock  = data.product.product_stock > 0;
  
	onMount(() => {
	  if (data.user) isLoggedIn = true;
	  relatedProducts = data.productData
		.filter(item => item.product_type === data.product.product_type && item.id !== data.product.id)
		.slice(0, 4);
	});
  
	function previousImage() {
	  if (data.product.image_urls?.length) {
		currentImageIndex =
		  (currentImageIndex - 1 + data.product.image_urls.length) %
		  data.product.image_urls.length;
	  }
	}
  
	function nextImage() {
	  if (data.product.image_urls?.length) {
		currentImageIndex = (currentImageIndex + 1) % data.product.image_urls.length;
	  }
	}
  
	function handleOptionSelect(option: string) {
	  selectedOption = option;
	}
  
	function handleAddToCart() {
	  if (!isLoggedIn || !isInStock) return;
	  //if (hasOptions && !selectedOption) return;
  
	  // Spread the existing product and tack on quantity + option
	  addToOrder({
		...data.product,
		quantity:       1,
		product_option: selectedOption
	  });
	}
</script>
  
  
  <div class="items-center justify-center bg-white dark:bg-black">
	<br>
	<div class="flex md:flex-row flex-col items-center justify-center p-4 gap-x-6">
  
	  <!-- Image + arrows -->
	  <div class="relative w-full md:w-1/2">
		<img
		  class="rounded-xl aspect-[21/12]"
		  src={data.product.image_urls[currentImageIndex]}
		  style="max-height: 400px; width: 100%; object-fit: contain;" />
		{#if data.product.image_urls?.length > 1}
		  <button
			on:click={previousImage}
			class="absolute left-2 top-1/2 transform -translate-y-1/2 text-2xl text-primary-500"
		  ><i class="fa-solid fa-chevron-left"></i></button>
		  <button
			on:click={nextImage}
			class="absolute right-2 top-1/2 transform -translate-y-1/2 text-2xl text-primary-500"
		  ><i class="fa-solid fa-chevron-right"></i></button>
		{/if}
	  </div>
  
	  <!-- Details + options + add button -->
	  <div class="flex flex-col space-y-1 md:w-1/2 w-full">
		<h1 class="text-lg sm:text-2xl md:text-4xl font-semibold">{data.product.name}</h1>
		<p class="text-md sm:text-lg md:text-xl dark:text-gray-400 text-gray-600">
		  by <span class="font-medium">{data.product.brand}</span> · <span class="italic">{data.product.product_type}</span>
		</p>
		<p class="text-md dark:text-gray-500 text-gray-500">{data.product.description}</p>
		<br>
  
		{#if hasOptions}
		  <div class="mt-2">
			<p class="text-lg font-semibold mb-1">Options:</p>
			<div class="flex flex-wrap gap-2">
			  {#each data.product.options as option}
				<button
				  type="button"
				  on:click={() => handleOptionSelect(option)}
				  class="px-3 py-1 rounded border transition
						 {selectedOption === option
						   ? 'bg-primary-500 text-white border-primary-500'
						   : 'bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200 border-transparent'}"
				>
				  {option}
				</button>
			  {/each}
			</div>
		  </div>
		{/if}
  
		<br><br>
		<div class="flex items-center justify-between mt-4">
		  <div class="border-2 border-black dark:border-white py-2 px-6 rounded-lg inline-block">
			<p class="text-lg font-bold">${data.product.price.toFixed(2)}</p>
		  </div>
		  <span class={isInStock ? "text-green-600 font-semibold text-xl" : "text-red-600 font-semibold text-xl"}>
			{isInStock ? 'In Stock' : 'Out of Stock'}
		  </span>
		</div>
		<br>
		<button
		  class="w-full bg-primary-500 text-white font-semibold py-2 rounded hover:bg-primary-600 transition
				 disabled:opacity-50 disabled:cursor-not-allowed"
		  on:click={handleAddToCart}
		  disabled={!isLoggedIn || !isInStock }
		>
		  Add to Cart
		</button>
	  </div>
	</div>
  
	<!-- Related items -->
	<div><br><p class="text-4xl text-center font-bold">Related Items</p></div><br>
	<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6">
	  {#each relatedProducts as product}
		<ProductCard
		  {product}
		  onProductSelect={() => goto(`/products/${product.id}`)}
		  {isLoggedIn} />
	  {/each}
	</div>
  </div>
  
