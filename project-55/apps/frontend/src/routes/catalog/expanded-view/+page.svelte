<script lang="ts">
  import { selectedProduct, addToOrder } from "$lib/stores/orders"; 
  import type { Product } from "$lib/stores/orders";
  import { onDestroy } from "svelte";
  import { page } from "$app/stores"; 

  let product: Product | null = null;

  // Subscribe to store reactively
  $: {
    selectedProduct.subscribe(value => {
      product = value;
    });
  }

  // Redirect only after checking store update
  onDestroy(() => {
    if (!product) {
      window.location.href = "/catalog";
    }
  });
</script>

<div class="flex flex-col items-center about-me w-full h-full overflow-y-auto">
  {#if product}
    <!-- Card with Primary Color -->
    <div class="max-w-2xl mx-auto text-center p-6 bg-primary-500 text-primary-50 shadow-lg rounded-lg">
      <h1 class="text-3xl font-bold">{product.name}</h1>

      <!-- Product Image -->
      <img 
        class="w-full max-h-96 object-contain rounded-lg mx-auto mt-4 bg-primary-300" 
        src={product.image} 
        alt={product.name} 
      />
      
      <!-- Price and Description -->
      <p class="text-lg font-semibold mt-4">${product.price.toFixed(2)}</p>
      <h3 class="text-xl font-semibold mt-4">Description:</h3>
      <p class="mt-2">{product.description}</p>
      
      <!-- Components List -->
      <h3 class="text-xl font-semibold mt-4">Components:</h3>
      <ul class="list-disc list-inside">
        {#each product.components as component}
          <li>{component}</li>
        {/each}
      </ul>

      <!-- Buttons (Stacked) -->
      <div class="flex flex-col gap-4 mt-6">
        <!-- Add to Cart Button -->
        <button 
          class="px-6 py-3 bg-white text-gray-800 border border-gray-400 rounded-lg hover:bg-gray-100 transition flex justify-center items-center text-center gap-2 w-full"
          on:click={() => product && addToOrder(product)}
        >
          🛒 Add to Cart
        </button>

        <!-- Back to Catalog Button -->
        <a href="/catalog" class="px-4 py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 transition">
          Back to Catalog
        </a>
      </div>

    </div>
  {:else}
    <p class="text-center text-lg">Loading product...</p>
  {/if}
</div>

