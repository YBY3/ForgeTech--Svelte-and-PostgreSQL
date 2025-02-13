<script lang="ts">
    import { orderStore, removeFromOrder } from "$lib/StoreOrders/orders";
  </script>
  
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-3xl font-bold text-center mb-6">Your Order</h1>
  
    {#if $orderStore.length === 0}
      <p class="text-center text-lg">Your order is empty. <a href="/catalog" class="text-blue-500">Browse Products</a></p>
    {:else}
      <ul class="space-y-4">
        {#each $orderStore as product, index}
          <li class="flex justify-between items-center p-4 border rounded-lg shadow-md">
            <div>
              <h2 class="text-lg font-semibold">{product.name}</h2>
              <p class="text-gray-600">${product.price.toFixed(2)}</p>
            </div>
            <button 
              class="text-red-500 hover:text-red-700 transition"
              on:click={() => removeFromOrder(product.id)}
            >
              ❌ Remove
            </button>
          </li>
        {/each}
      </ul>
  
      <!-- Total Price -->
      <div class="mt-6 text-center">
        <p class="text-xl font-semibold">Total: ${$orderStore.reduce((sum, item) => sum + item.price, 0).toFixed(2)}</p>
      </div>
    {/if}
  </div>
  
  