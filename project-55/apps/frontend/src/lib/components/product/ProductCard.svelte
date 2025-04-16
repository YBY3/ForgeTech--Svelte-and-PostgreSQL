<script lang="ts">
  import type { ProductType } from "$lib/types/ProductTypes";
  import { addToOrder } from "$lib/stores/OrdersStore";

  export let product: ProductType;
  export let onProductSelect: ((product: ProductType) => void) | null = null;
  export let detailedView: boolean = false;
  export let isLoggedIn = false;

  const isInStock = product.product_stock > 0;
</script>

<div class="w-full max-w-md bg-white dark:bg-black border-gray-300 border-2 dark:border-gray-800 rounded-lg p-4">
  <!-- Product Image -->
  <div class="w-full h-64 rounded-lg overflow-hidden mb-4 cursor-pointer" on:click={() => onProductSelect && onProductSelect(product)}>
    <img src={product.image_urls[0]} alt={product.name} class="w-full h-full object-cover transition duration-200 hover:scale-105" />
  </div>

  <!-- Product Details -->
  <div class="flex flex-col space-y-1">
    <h2 class="text-xl font-semibold truncate">{product.name}</h2>
    <p class="text-sm dark:text-gray-400 text-gray-600 truncate">by <span class="font-medium">{product.brand}</span> · <span class="italic">{product.product_type}</span></p>
    <p class="text-sm dark:text-gray-500 text-gray-500 truncate">{product.description}</p>

    <!-- Options -->
    {#if product.options && product.options.length > 0}
      <div class="mt-2">
        <p class="text-sm font-semibold mb-1">Options:</p>
        <div class="flex flex-wrap gap-2">
          {#each product.options as option}
            <span class="px-2 py-1 bg-gray-200 dark:bg-gray-800 rounded text-xs">{option}</span>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Stock & Price -->
    <div class="flex items-center justify-between mt-4">
      <p class="text-lg font-bold">${product.price.toFixed(2)}</p>
      <span class={isInStock ? "text-green-600 font-semibold" : "text-red-600 font-semibold"}>
        {isInStock ? 'In Stock' : 'Out of Stock'}
      </span>
    </div>

<!-- Add to Cart Button -->
<div class="mt-4">
  <button 
    class="w-full bg-primary-500 text-white font-semibold py-2 rounded hover:bg-primary-600 transition"
    on:click={() => addToOrder(product)}
    disabled={!isLoggedIn || !isInStock}
  >
    Add to Cart
  </button>
</div>

  </div>
</div>
