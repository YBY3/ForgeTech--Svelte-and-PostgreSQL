<script lang="ts">
    import { onMount } from 'svelte';
	import { Avatar, FileButton } from "@skeletonlabs/skeleton";
    import { ordersStore, removeFromOrder } from "$lib/stores/OrdersStore";
    import type { UserType } from '$lib/types/UserTypes';

    //User Data
    export let data;
    let userData: UserType;
    
    onMount(() => {
		if (data.user) {
			userData = data.user;
		}
	});
</script>


{#if userData} 
    <div class="h-full overflow-y-auto">
        <div class="flex flex-col items-center justify-center space-y-3 md:space-x-6">
            <br>
            <h1 class="text-3xl sm:text-4xl md:text-4xl">{userData.name}</h1>
            <br>
            <h1 class="text-xl">Profile Picture</h1>
            <Avatar initials="JD" background="bg-primary-500" width="w-32" />
            <FileButton name="files" class="px-4" accept="image/*">Edit</FileButton>
        </div>
        <br>
        <hr class="border-t w-full mx-auto">
        <br>
        <div class="flex flex-col items-center justify-center space-y-7 text-center">
            <h1 class="text-xl">{userData.username}</h1>
            <h1 class="text-xl">{userData.email}</h1>
            <h1 class="text-xl">Role: {userData.user_type}</h1>
        </div>
        <br>
        <hr class="border-t w-full mx-auto">
        <br>

        <div class="flex flex-col items-center justify-center space-y-7 text-center">
            <!-- <h1 class="text-xl">What will you be using Forge Tech for?</h1>
            <select class="select w-64 ml-4">
                <option>Select</option>            
                <option value="1">Business</option>
                <option value="2">Customer</option>
            </select> -->
        </div>
        <br>
        <br>
        <div class="flex flex-col items-center"><h1 class="text-3xl sm:text-4xl md:text-4xl">Your Orders</h1></div>
        {#if $ordersStore.length === 0}
        <p class="text-center text-lg">Your order is empty. <a href="/catalog" class="text-blue-500">Browse Products</a></p>

    {:else}
        <ul class="space-y-4 p-12">
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
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
    </div>
{/if}