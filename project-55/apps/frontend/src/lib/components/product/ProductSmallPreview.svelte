<script lang="ts">
    import type { ProductPreviewType } from "$lib/types/ProductTypes"
    import { createEventDispatcher } from "svelte";

    //Tailwind Classes
    let overlayButtonClass = " w-1/3 btn text-lg font-bold rounded-lg ";

    export let showOverlay = false;
    export let product: ProductPreviewType;

    const dispatch = createEventDispatcher();
    const handleEdit = () => dispatch("edit", { product });
    const handleDelete = () => dispatch("delete", { product });
</script>


<div class="relative w-full h-auto grid grid-cols-[50px_1fr_100px] gap-4 place-items-center justify-items-center card variant-ghost card-hover rounded-lg p-4 group">
    <div class="font-semibold text-black-800">{product.id}</div>
    <h2 class="text-lg font-semibold text-black-800">{product.name}</h2>
    <div class="font-semibold text-black-800">${product.price}</div>

    <!-- Hover Overlay -->
    {#if showOverlay}
        <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg">
            <button class="{overlayButtonClass} variant-filled-secondary" on:click={handleEdit}>Edit</button>
            <button class="{overlayButtonClass} variant-filled-primary" on:click={handleDelete}>Delete</button>
        </div>
    {/if}
</div>