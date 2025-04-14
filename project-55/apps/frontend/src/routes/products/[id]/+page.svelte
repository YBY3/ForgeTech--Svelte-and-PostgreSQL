<script lang="ts">
    import ProductCard from '$lib/components/product/ProductCard.svelte';
    import type { ProductType } from '$lib/types/ProductTypes';
    import { addToOrder } from "$lib/stores/OrdersStore";
	import { onMount } from 'svelte';
    export let isLoggedIn = false;
    export let data: {
		 user: any; product: ProductType, isLoggedIn: boolean 
    };

    const isInStock = data.product.product_stock > 0;

    onMount(() => {
      if (data.user) {
        isLoggedIn = true;
      }
      
    });

  </script>
  
<div class="items-center justify-center">
  <div class="flex md:flex-row flex-col items-center justify-center p-8 gap-x-6">

    <div class="w-full lg:w-1/2">
        <img src={data.product.image_urls[0]}>
    </div>
    <div class="flex flex-col space-y-1">
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
</div>