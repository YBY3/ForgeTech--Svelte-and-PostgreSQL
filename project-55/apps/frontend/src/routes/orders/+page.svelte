<script lang="ts">
    import { ordersStore, removeFromOrder } from "$lib/stores/OrdersStore";
</script>

<div class="h-full overflow-y-auto">
    <div class="max-w-2xl mx-auto p-6"> 
        <h1 class="text-3xl font-bold text-center mb-6">Your Order</h1>

        {#if $ordersStore.length === 0}
            <p class="text-center text-lg">Your order is empty. <a href="/catalog" class="text-blue-500">Browse Products</a></p>

        {:else}
            <ul class="space-y-4">
            {#each $ordersStore as product, index}
                <li class="flex items-center justify-between p-4 border rounded-lg shadow-md">

                    <!-- Image & Product Info Section -->
                    <div class="flex items-center gap-4">
                        <!-- Product Image (Left) -->
                        <img 
                        class="w-16 h-16 object-contain rounded-md bg-gray-100" 
                        src={product.image} 
                        alt={product.name}
                        />

                        <!-- Product Name & Price -->
                        <div>
                            <h2 class="text-lg font-semibold">{product.name}</h2>
                            <p class="text-gray-600">${product.price.toFixed(2)}</p>
                        </div>
                    </div>

                    <!-- Remove Button (Right) -->
                    <button 
                        class="text-red-500 hover:text-red-700 transition"
                        on:click={() => removeFromOrder(product.id)}
                        >
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </li>
            {/each}
            </ul>

            <!-- Total Price -->
            <div class="mt-6 text-center">
                <p class="text-xl font-semibold">Total: ${$ordersStore.reduce((sum, item) => sum + item.price, 0).toFixed(2)}</p>
            </div>
            <br>
            <br>
            <br>
        {/if}
    </div>
</div>