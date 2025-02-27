<script lang="ts">
    import { ordersStore, removeFromOrder } from "$lib/stores/OrdersStore";
</script>

<div class="h-full overflow-y-auto">
    <div class="max-w-5xl mx-auto p-6"> 
        <h1 class="text-3xl font-bold text-center mb-6">Shopping Cart</h1>
        <br>
        {#if $ordersStore.length === 0}
            <p class="text-center text-lg">Your cart is empty. <a href="/catalog" class="text-blue-500">Browse Products</a></p>

        {:else}
            <div class="flex items-center w-full justify-center">
                <div class="flex flex-col items-center">
                    <div class="p-2 px-4 sm:p-6 sm:px-8 bg-primary-500 rounded-full text-2xl">1</div>
                    <span class="text-center text-xs sm:text-lg">Orders</span>
                </div>
                <hr class="border-t w-full mx-auto">
                <div class="flex flex-col items-center">
                    <div class="p-2 px-4 sm:p-6 sm:px-8 bg-surface-200 dark:bg-surface-600 rounded-full text-2xl">2</div>
                    <span class="text-center text-xs sm:text-lg">Delivery/Payment</span>
                </div>
                <hr class="border-t w-full mx-auto">
                <div class="flex flex-col items-center">
                    <div class="p-2 px-4 sm:p-6 sm:px-8 bg-surface-200 dark:bg-surface-600 rounded-full text-2xl">3</div>
                    <span class="text-center text-xs sm:text-lg">Confirmation</span>
                </div>
            </div>
            <br>
            <br>
            <ul class="space-y-4">
            {#each $ordersStore as product, index}
                <li class="flex items-center justify-between p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover">

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
            <div class="text-center"><button type="button" class="btn border-2 border-primary-500 text-white rounded-lg bg-primary-500 px-8 py-3 hover: transition-all duration-300 ease-in-out hover:shadow-[0_0_20px_5px_rgba(212,22,60,0.7)]">Proceed to Checkout</button></div>
            <br>
            <br>
            <br>
        {/if}
    </div>
</div>