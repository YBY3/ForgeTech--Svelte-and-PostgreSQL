<script lang="ts">
    import { selectedProduct } from "$lib/StoreOrders/orders"; // ✅ Import selected product store
    import type { Product } from "$lib/StoreOrders/orders";
    import { get } from "svelte/store";
  
    let product: Product | null = get(selectedProduct); // Get selected product
  
    // Redirect to catalog if no product is selected (e.g., page was refreshed)
    if (!product) {
      window.location.href = "/catalog"; // ✅ Redirects user if they land here without selecting a product
    }
  </script>
  
<div class="flex flex-col items-center w-full h-full overflow-y-auto">
  {#if product}
    <div class="max-w-2xl mx-auto text-center p-6">
      <h1 class="text-3xl font-bold">{product.name}</h1>
      <img class="w-full max-h-96 object-cover rounded-lg mx-auto mt-4" src={product.image} alt={product.name} />
      
      <p class="text-lg font-semibold text-gray-900 mt-4">${product.price.toFixed(2)}</p>
      <p class="text-gray-600 mt-2">{product.description}</p>
      
      <h3 class="text-xl font-semibold mt-4">Components:</h3>
      <ul class="text-gray-700">
        {#each product.components as component}
          <li>- {component}</li>
        {/each}
      </ul>
  
      <a href="/catalog" class="mt-6 inline-block px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
        Back to Catalog
      </a>
    </div>
  {:else}
    <p class="text-center text-lg">Loading product...</p>
  {/if}
</div>