<script lang="ts">
  import type { ProductType } from "$lib/types/ProductTypes";
  import { addToOrder } from "$lib/stores/OrdersStore";

  export let product: ProductType;
  export let onProductSelect: ((product: ProductType) => void) | null = null;
  export let detailedView: boolean = false;
  export let isLoggedIn = false;

</script>

<div class="w-full relative border border-gray-600 card-hover rounded-none shadow-md p-2 flex flex-col justify-between hover:bg-gray-200 hover:bg-opacity-5">
  
  <!-- Clickable Product Image (Only if not in detailed view) -->
  {#if !detailedView}
    <button 
      class="w-full h-80 flex items-center justify-center bg-gray-200 rounded-md"
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
   <br>
  <div class="flex flex-col flex-grow justify-between">
    <h2 class="text-lg font-bold text-black-800 px-2">{product.name}</h2>
    <p class="text-black-600 text-sm truncate px-2">{product.description}</p>

    <!-- Extra Details (Only in Detailed View) -->
    {#if detailedView}
      <div>
        
        <img 
            class="w-full h-full object-cover rounded-md" 
            src={product.image} 
            alt={product.name}
        />
      </div>
      <h3 class="text-xl font-semibold">Components:</h3>
      <ul class="list-disc list-inside">
        {#each product.components as component}
          <li>{component}</li>
        {/each}
      </ul>
    {/if}

    <!-- Price & Cart Button Section -->
    <div class="flex justify-between items-center mt-4 px-2 py-2">
      <p class="text-lg font-bold">${product.price.toFixed(2)}</p>

      <!-- Add to Cart Button with Tooltip -->
      <div class="relative group">
        <button 
          class="w-10 h-10 border border-2 border-black dark:border-white rounded-md flex items-center justify-center hover:bg-primary-500 transition hover:border-none hover:shadow-[0_0_20px_5px_rgba(212,22,60,0.7)] disabled:opacity-50 disabled:cursor-not-allowed"
          on:click={() => addToOrder(product)} disabled={!isLoggedIn}
        >
        <i class="fa-solid fa-cart-shopping"></i>
        </button>

        <!-- Tooltip Above -->
        <span class="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-black text-white text-sm px-3 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
          {#if isLoggedIn}
              Add to Cart
          {:else}
              Login 
          {/if}
        </span>
      </div>
    </div>
  </div>
</div>