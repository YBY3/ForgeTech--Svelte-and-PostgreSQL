<script lang="ts">
    import type { ProductPreviewType } from "$lib/types/ProductTypes";
    import { createEventDispatcher } from "svelte";
  
    // Props:
    // - product: the product data
    // - showOverlay: whether to display overlay actions (default false)
    // - orderDisplay: if true, disable individual hover effects (for order display context)
    export let product: ProductPreviewType;
    export let showOverlay: boolean = false;
    export let orderDisplay: boolean = false;
  
    const dispatch = createEventDispatcher();
    const handleEdit = () => dispatch("edit", { product });
    const handleDelete = () => dispatch("delete", { product });
  </script>
  
  <!-- 
    Conditionally add hover classes only when not in orderDisplay mode.
    When orderDisplay is true, the component remains static.
  -->
  <div class={`relative w-full h-auto grid grid-cols-[50px_1fr] gap-4 place-items-center justify-items-center card variant-ghost ${orderDisplay ? '' : 'card-hover'} rounded-lg p-4 ${orderDisplay ? '' : 'group'}`}>
    <!-- First Column: Display quantity if available (in orderDisplay mode) or product id otherwise -->
    <div class="font-semibold text-black-800">
      {#if orderDisplay && product.quantity !== undefined}
        <span class="text-sm">x{product.quantity}</span>
      {:else}
        {product.id}
      {/if}
    </div>
    
    <!-- Second Column: Product Name -->
    <div class="w-full">
      <h2 class="text-lg font-semibold text-black-800">{product.name}</h2>
    </div>
  
    <!-- Optional Hover Overlay: Only shown if showOverlay is true and not in orderDisplay mode -->
    {#if showOverlay && !orderDisplay}
      <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg">
        <button class="w-1/3 btn text-lg font-bold rounded-lg variant-filled-secondary" on:click={handleEdit}>Edit</button>
        <button class="w-1/3 btn text-lg font-bold rounded-lg variant-filled-primary" on:click={handleDelete}>Delete</button>
      </div>
    {/if}
  </div>  