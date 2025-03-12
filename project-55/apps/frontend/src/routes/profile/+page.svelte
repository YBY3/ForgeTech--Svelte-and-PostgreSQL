<script lang="ts">
	import { onMount } from 'svelte';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { Avatar, FileButton } from "@skeletonlabs/skeleton";
	import ProductSmallPreview from '$lib/components/product/ProductSmallPreview.svelte';
	import type { UserType } from '$lib/types/UserTypes';
	import type { PastOrderType } from '$lib/types/OrderTypes.js';

	// User Data
	export let data;
	let userData: UserType;
	let pastOrders: PastOrderType[];
	let isEmployee: boolean = false;
	
	// Page Elements (Toast Notifications)
	const toastStore = getToastStore();

	onMount(() => {
		if (data.user) {
			userData = data.user;
			isEmployee = userData.user_type === 'employee'; // Check if user is employee
		}
		if (data.pastOrders) {
			// pastOrders = data.pastOrders;
			pastOrders = data.pastOrders.sort((a, b) => b.id - a.id);

		}
		if (data.error) {
			toastStore.trigger({
				message: data.error,
				background: 'variant-filled-error'
			});
		}
	});

	/**
	 * Groups duplicate products and adds a quantity field.
	 * @param products Array of product objects from an order.
	 * @returns Array of unique products, each with a quantity field.
	 */
	function groupProducts(products: any[]): any[] {
		const grouped: Record<string, any> = {};
		for (const product of products) {
			if (grouped[product.id]) {
				grouped[product.id].quantity++;
			} else {
				grouped[product.id] = { ...product, quantity: 1 };
			}
		}
		return Object.values(grouped);
	}
</script>


{#if userData} 
	<div class="h-full overflow-y-auto">
		<!-- Profile Section -->
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

		<!-- User Info Section -->
		<div class="flex flex-col items-center justify-center space-y-7 text-center">
			<h1 class="text-xl">{userData.username}</h1>
			<h1 class="text-xl">{userData.email}</h1>
			<h1 class="text-xl">Role: {userData.user_type}</h1>
		</div>

		<br>
		<hr class="border-t w-full mx-auto">
		<br>

		<!-- (Optional) Extra Profile Settings -->
		<div class="flex flex-col items-center justify-center space-y-7 text-center">
			<!-- Additional settings or selections can be added here -->
		</div>

		<br>
		<br>

		<!-- placeholder for claimed orders -->
		 
		<!-- Conditional Employee Section -->
        <!-- {#if isEmployee}
            <div class="flex flex-col items-center">
                <h1 class="text-2xl font-semibold">Employee Dashboard</h1>
                <p class="text-lg text-gray-700">Welcome, {userData.name}! You can manage orders under here.</p> -->

                <!-- Placeholder for Claimed Orders -->
                <!-- <div class="mt-4 p-4 border border-gray-300 rounded-lg">
                    <h2 class="text-xl font-semibold">Claimed Customer Orders</h2>
                    <p class="text-gray-600 italic">Feature coming soon...</p>
                </div> 
				<br><br>
            </div>
        {/if} -->

		<!-- Prep for employee order claims -->
		{#if isEmployee}
    	<div class="flex flex-col items-center">
			<h1 class="text-2xl font-semibold">Employee Dashboard</h1>
			<p class="text-lg text-gray-700">Welcome, {userData.name}! You can see your claimed orders here.</p>

			<!-- Display claimed orders -->
			<div class="mt-4 p-4 border border-gray-300 rounded-lg">
				<h2 class="text-xl font-semibold">Claimed Orders</h2>
				{#if pastOrders && pastOrders.length > 0}
					<ul>
						{#each pastOrders as order (order.id)}
							<div class="flex flex-col gap-2 items-center card variant-ringed p-4">
								<li>
									<strong>Order ID:</strong> {order.id} <br>
									<strong>Total:</strong> ${order.total} <br>
									<strong>Status:</strong> {order.status} <br>
									<strong>Products:</strong>
									<ul class="mt-2">
										{#each groupProducts(order.products) as product}
											<li class="flex items-center gap-2">
												<ProductSmallPreview product={product} />
												<span class="font-semibold text-black-800">x{product.quantity}</span>
											</li>
										{/each}
									</ul>
								</li>
								<hr class="w-full border-t">
							</div>
						{/each}
					</ul>
				{:else}
					<p class="text-center text-lg text-gray-600">No claimed orders yet :/ </p>
				{/if}
			</div>
		</div>
		{/if}


		{#if !isEmployee}
		<!-- Past Orders Section -->
		<div class="flex flex-col items-center">
			<h1 class="text-3xl sm:text-4xl md:text-4xl">Past Orders</h1>
            <br>
			{#if pastOrders}
				<ul>
					{#each pastOrders as order (order.id)}
						<div class="flex flex-col gap-2 items-center card variant-ringed p-4">
							<li>
								<strong>Order ID:</strong> {order.id} <br>
								<strong>Total:</strong> ${order.total} <br>
								<strong>Status:</strong> {order.status} <br>
								<strong>Products:</strong>
								<ul class="mt-2">
									{#each groupProducts(order.products) as product}
										<li class="flex items-center gap-2">
											<ProductSmallPreview product={product} />
                                            <span class="font-semibold text-black-800">x{product.quantity}</span>
										</li>
									{/each}
								</ul>
							</li>
							<hr class="w-full border-t">
						</div>
					{/each}
				</ul>
			{:else}
				<p class="text-center text-lg">
					Your order is empty. <a href="/catalog" class="text-blue-500">Browse Products</a>
				</p>
			{/if}
		</div>
		{/if}
		
	</div>
{/if}