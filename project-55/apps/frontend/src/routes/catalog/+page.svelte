<script lang="ts">
  import { productStore, selectedProduct } from "$lib/stores/orders"; 
  import type { Product } from "$lib/stores/orders"; // Import Product type
  import { writable } from "svelte/store";

  // Use $productStore to access store reactively
  let products = $productStore;

  function selectProduct(product: Product) {  // Explicitly type 'product'
    selectedProduct.set(product);
  }

  // import { productStore } from "$lib/StoreOrders/orders"; 
  import { addToOrder } from "$lib/stores/orders"; 
</script>

<div class="flex flex-col items-center w-full h-full overflow-y-auto">
  <br>
  <h1 class="text-center text-4xl font-medium">Our Products</h1>
  <br>

  <!-- Catalog Grid -->
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6">
    {#each $productStore as product}
      <div class="relative card variant-filled-primary card-hover rounded-lg shadow-md p-4">
        
        <!-- Make Image Clickable -->
        <a href="/catalog/expanded-view" on:click={() => selectProduct(product)}>
          <div class="w-full h-60 flex items-center justify-center bg-gray-200">
            <img 
              class="max-h-full max-w-full object-contain rounded-md cursor-pointer" 
              src={product.image} 
              alt={product.name}
            />
          </div>
        </a>  
        
        <br>

        <h2 class="text-lg font-semibold text-black-800">{product.name}</h2>
        <p class="text-black-600 text-sm">{product.description}</p>
        <!-- Price & Cart Button Section -->
        <div class="flex justify-between items-center mt-4">
          <p class="text-lg font-semibold text-gray-900">${product.price.toFixed(2)}</p>
          
        <!-- Add to Cart Button with Tooltip -->
    <div class="relative group">
      <button 
        class="w-10 h-10 bg-white border border-gray-300 rounded-md flex items-center justify-center hover:bg-gray-100 transition"
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
    {/each}
  </div>  
</div>


