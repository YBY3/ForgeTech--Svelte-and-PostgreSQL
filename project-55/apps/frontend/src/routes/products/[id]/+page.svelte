<script lang="ts">
    import ProductCard from '$lib/components/product/ProductCard.svelte';
    import type { ProductType } from '$lib/types/ProductTypes';
    import { addToOrder } from "$lib/stores/OrdersStore";
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
    export let isLoggedIn = false;
    export let data: {
		 user: any; product: ProductType, isLoggedIn: boolean, productData: ProductType[] 
    };
    let relatedProducts: ProductType[] = [];

    const isInStock = data.product.product_stock > 0;

    onMount(() => {
      if (data.user) {
        isLoggedIn = true;
      }

      data.productData.filter
      relatedProducts = data.productData.filter(
    (item) => item.product_type === data.product.product_type && item.id !== data.product.id
  );
    });

  </script>
  
<div class="items-center justify-center px-2">
    <br>
  <div class="flex md:flex-row flex-col items-center justify-center p-8 gap-x-6 bg-white dark:bg-black rounded-xl">

    <div class="w-full md:w-1/2">
        <img class="rounded-xl border-2 dark:border-white border-black" src={data.product.image_urls[0]}>
    </div>
    <br>
    <div class="flex flex-col space-y-1 md:w-1/2 w-full">
        <h1 class="text-lg sm:text-2xl md:text-4xl font-semibold">{data.product.name}</h1>
        <p class="text-md sm:text-lg md:text-xl dark:text-gray-400 text-gray-600">by <span class="font-medium">{data.product.brand}</span> · <span class="italic">{data.product.product_type}</span></p>
        <p class="text-md dark:text-gray-500 text-gray-500 truncate">{data.product.description}</p>
        <br>
        {#if data.product.options && data.product.options.length > 0}
            <div class="mt-2">
                <p class="text-lg font-semibold mb-1">Options:</p>
                <div class="flex flex-wrap gap-2">
                {#each data.product.options as option}
                    <span class="px-2 py-1 bg-gray-200 dark:bg-gray-800 rounded text-md">{option}</span>
                {/each}
                </div>
            </div>
        {/if}
        <br>
        <br>
        <div class="flex items-center justify-between mt-4">
            <div class="border-2 border-black dark:border-white py-2 px-6 rounded-lg inline-block"><p class="text-lg font-bold">${data.product.price.toFixed(2)}</p></div>
            <span class={isInStock ? "text-green-600 font-semibold text-xl" : "text-red-600 font-semibold text-xl"}>
              {isInStock ? 'In Stock' : 'Out of Stock'}
            </span>
        </div>
        <br>
        <button 
            class="w-full bg-primary-500 text-white font-semibold py-2 rounded hover:bg-primary-600 transition"
            on:click={() => addToOrder(data.product)}
            disabled={!isLoggedIn || !isInStock}
            >
            Add to Cart
        </button>
    </div>
  </div>
  <div>
    <br>
    <p class="text-4xl text-center font-bold">Related Items</p>
  </div>
  <br>
  <hr class="border-t border-white w-full w-3/4 mx-auto">
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6">
    {#each relatedProducts as product}
      <ProductCard 
      product={product} 
      onProductSelect={(product) => window.location.href = `/products/${product.id}`}
      isLoggedIn={isLoggedIn}
      />
    {/each}
  </div>  
</div>