<script lang="ts">
  import type { ProductType } from "$lib/types/ProductTypes";
  import { addToOrder } from "$lib/stores/OrdersStore";

  export let product: ProductType;
  export let onProductSelect: ((product: ProductType) => void) | null = null;
  export let detailedView: boolean = false;
  export let isLoggedIn = false;

  const isInStock = product.product_stock > 0;
</script>

<div class="w-full max-w-md bg-white text-black border border-gray-300 rounded-lg shadow-lg p-4 hover:shadow-xl transition duration-200">
  <!-- Product Image -->
  <div class="w-full h-64 bg-gray-100 rounded-lg overflow-hidden mb-4 cursor-pointer" on:click={() => onProductSelect && onProductSelect(product)}>
    <img src={product.image_urls[0]} alt={product.name} class="w-full h-full object-cover transition duration-200 hover:scale-105" />
  </div>

  <!-- Product Details -->
  <div class="flex flex-col space-y-1">
    <h2 class="text-xl font-semibold">{product.name}</h2>
    <p class="text-sm text-gray-600">by <span class="font-medium">{product.brand}</span> · <span class="italic">{product.product_type}</span></p>
    <p class="text-sm text-gray-700 truncate">{product.description}</p>

    <!-- Options -->
    {#if product.options && product.options.length > 0}
      <div class="mt-2">
        <p class="text-sm font-semibold mb-1">Options:</p>
        <div class="flex flex-wrap gap-2">
          {#each product.options as option}
            <span class="px-2 py-1 bg-gray-200 rounded text-xs">{option}</span>
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
    class="w-full bg-red-600 text-white font-semibold py-2 rounded hover:bg-red-700 transition"
    on:click={() => addToOrder(product)}
    disabled={!isLoggedIn || !isInStock}
  >
    Add to Cart
  </button>
</div>

  </div>
</div>
