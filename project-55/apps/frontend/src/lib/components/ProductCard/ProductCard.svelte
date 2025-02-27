<script lang="ts">
  import type { ProductType } from "$lib/types/ProductTypes";
  import { addToOrder } from "$lib/stores/OrdersStore";

  export let product: ProductType;
  export let onProductSelect: ((product: ProductType) => void) | null = null;
  export let detailedView: boolean = false;
</script>

<div class="w-full relative card variant-filled-primary card-hover rounded-lg shadow-md p-4 h-[400px] flex flex-col justify-between">
  
  <!-- Clickable Product Image (Only if not in detailed view) -->
  {#if !detailedView}
    <button 
      class="w-full h-40 flex items-center justify-center bg-gray-200 rounded-md"
      on:click={() => onProductSelect && onProductSelect(product)}
    >
      <!-- Ensure consistent image size -->
      <img 
        class="w-full h-full object-cover rounded-md" 
        src={product.image} 
        alt={product.name}
      />
    </button>  
  {/if}

  <!-- Product Details -->
  <div class="flex flex-col flex-grow justify-between">
    <h2 class="text-lg font-semibold text-black-800">{product.name}</h2>
    <p class="text-black-600 text-sm truncate">{product.description}</p>

    <!-- Extra Details (Only in Detailed View) -->
    {#if detailedView}
      <h3 class="text-xl font-semibold mt-4">Components:</h3>
      <ul class="list-disc list-inside">
        {#each product.components as component}
          <li>{component}</li>
        {/each}
      </ul>
    {/if}

    <!-- Price & Cart Button Section -->
    <div class="flex justify-between items-center mt-4">
      <p class="text-lg font-semibold text-gray-900">${product.price.toFixed(2)}</p>

      <!-- Add to Cart Button with Tooltip -->
      <div class="relative group">
        <button 
          class="w-10 h-10 bg-white border border-gray-300 rounded-md flex items-center justify-center hover:bg-gray-100 transition shadow-lg"
          on:click={() => addToOrder(product)}
        >
          🛒
        </button>

        <!-- Tooltip Above -->
        <span class="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-black text-white text-sm px-3 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
          Add to Cart
        </span>
      </div>
    </div>
  </div>
</div>