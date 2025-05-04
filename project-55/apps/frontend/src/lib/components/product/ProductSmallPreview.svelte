<script lang="ts">
    import type { ProductPreviewType } from '$lib/types/ProductTypes';
    import { createEventDispatcher } from 'svelte';
  
    let overlayButtonClass = 'w-1/3 btn text-lg font-bold rounded-lg';
  
    export let showOverlay = false;
    export let product: ProductPreviewType & { quantity?: number };
  
    const dispatch = createEventDispatcher();
    const handleEdit = () => dispatch('edit', { product });
    const handleDelete = () => dispatch('delete', { product });
  </script>
  
  <div class="relative w-full
          flex flex-col items-center text-center space-y-1
          card variant-ghost card-hover rounded-lg p-4 group"
  >
    <!-- Product name -->
    <h2 class="text-lg font-semibold text-black-800">{product.name}</h2>
  
    <!-- Qty or price, no background -->
    {#if product.quantity !== undefined}
      <div class="text-black-800 text-sm font-medium">
        ${product.price} <br>
        Qty: {product.quantity}
      </div>
    <!-- {:else}
      <div class="font-semibold text-black-800">${product.price}</div> -->
    {/if}
  
    {#if showOverlay}
      <div
        class="absolute inset-0 bg-black bg-opacity-50
               flex items-center justify-center gap-2
               opacity-0 group-hover:opacity-100
               transition-opacity duration-300 rounded-lg"
      >
        <button class="{overlayButtonClass} variant-filled-secondary" on:click={handleEdit}>
          Edit
        </button>
        <button class="{overlayButtonClass} variant-filled-primary" on:click={handleDelete}>
          Delete
        </button>
      </div>
    {/if}
  </div>
  