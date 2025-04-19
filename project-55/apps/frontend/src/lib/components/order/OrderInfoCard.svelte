<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import ProductSmallPreview from '$lib/components/product/ProductSmallPreview.svelte';
    import type { OrderType } from '$lib/types/OrderTypes';
    import type { ProductOrderPreviewType } from '$lib/types/ProductTypes';

    //Data
    export let order: OrderType;
    let products: ProductOrderPreviewType[] = order.products;

    //Component Elements
    export let showCancelButton = false;
    export let showClaimButton = false;
    const dispatch = createEventDispatcher();

    function handleCancelButtonClick(orderID: number) {
        dispatch('cancelRequest', { orderID: orderID });
    }

    function handleClaimButtonClick(orderID: number, orderStatus: string) {
        dispatch('claimRequest', { orderID: orderID, orderStatus: orderStatus  });
    }
</script>


{#if order}

    <div class="w-full flex flex-col items-center gap-2 card variant-surface p-3">

        <!-- Order Info -->
        <strong>Created: {new Date(order.created_at).toLocaleString()}</strong>
   
        <div class="w-full flex flex-col items-start text-center rounded-lg gap-1 pl-4 pr-4 pb-1 pt-1">
            <div>Order Info:</div>
            <div>Total: ${order.total}</div>
            <div>Status: {order.status}</div>
        </div>

        <div class="w-full p-2 rounded-lg">
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
        </div>
        
        {#if showCancelButton}
            <button 
                class="w-1/2 flex flex-col btn variant-filled-primary text-lg text-center font-semibold cursor-grab rounded-lg gap-4 p-1"
                on:click={() => handleCancelButtonClick(order.id)}
            >
                Cancel Order
            </button>
        {/if}

        {#if showClaimButton}
            {#if order.status == "pending"}
                <button 
                    class="w-1/2 flex flex-col btn variant-filled-success text-lg text-center font-semibold cursor-grab rounded-lg gap-4 p-1"
                    on:click={() => handleClaimButtonClick(order.id, order.status)}
                >
                    Claim Order
                </button>
            {:else}
                <button 
                    class="w-1/2 flex flex-col btn variant-filled-primary text-lg text-center font-semibold cursor-grab rounded-lg gap-4 p-1"
                    on:click={() => handleClaimButtonClick(order.id, order.status)}
                >
                    Unclaim Order
                </button>
            {/if}
        {/if}
    </div>

{/if}