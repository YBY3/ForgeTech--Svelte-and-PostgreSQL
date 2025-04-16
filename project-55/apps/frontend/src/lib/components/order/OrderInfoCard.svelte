<script lang="ts">
    import ProductSmallPreview from '$lib/components/product/ProductSmallPreview.svelte';
    import type { OrderType } from '$lib/types/OrderTypes';
    import type { ProductOrderPreviewType } from '$lib/types/ProductTypes';

    export let order: OrderType;
    let products: ProductOrderPreviewType[] = order.products;

    export let showCancelButton = false;
</script>


{#if order}

    <div class="w-full flex flex-col items-center gap-3 card variant-ringed p-3">

        <!-- Order Info -->
        <strong>Created: {new Date(order.created_at).toLocaleString()}</strong>
        <div class="w-full flex gap-3">
            <div class="w-full flex flex-col card variant-filled text-center rounded-lg gap-4 p-1">
                Total: ${order.total}
            </div>
            <div class="w-full flex flex-col card variant-filled text-center rounded-lg gap-4 p-1">
                Status: {order.status}
            </div>
        </div>

        {#if products.length > 0}
            <!-- Ordered Products -->
            {#each order.products as product (product.id)}

                <div class="w-full flex gap-3 items-center pl-3 pr-3">
                    <ProductSmallPreview product={product} />
                    <span class="font-semibold text-black-800">x{product.quantity}</span>
                </div>
            
            {/each}
        {:else}
            
            <!-- No Products -->
            <div class="w-full flex flex-col card variant-ghost text-lg text-center font-semibold rounded-lg gap-4 p-4">
                No Products Found
            </div>

        {/if}
        
        {#if showCancelButton}
            <div class="w-1/2 flex flex-col btn variant-filled-primary text-lg text-center font-semibold rounded-lg gap-4 p-1">
                Cancel Order Request
            </div>
        {/if}
    </div>

{/if}