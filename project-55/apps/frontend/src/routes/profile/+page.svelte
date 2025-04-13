<script lang="ts">
	import { onMount } from 'svelte';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { Avatar, FileButton } from "@skeletonlabs/skeleton";
	import ProductSmallPreview from '$lib/components/product/ProductSmallPreview.svelte';
	import type { UserType } from '$lib/types/UserTypes';
	import type { PastOrderType } from '$lib/types/OrderTypes';

	// User Data from the load function
	export let data;
	let userData: UserType;

	// This variable will hold either claimed orders (for employees) or past orders (for customers)
	let pastOrders: PastOrderType[] = [];
	let isEmployee: boolean = false;
	let isAdmin: boolean = false;
	let isCustomer: boolean = false;
	
	// Admin Dashboard
	let recentUsers: any[] = [];
	let activeEmployees: any[] = [];
	let allRecentOrders: PastOrderType[] = [];

	
	// Page Elements (Toast Notifications)
	const toastStore = getToastStore();

	onMount(() => {
		if (data.user) {
			userData = data.user;
			isEmployee = userData.user_type === 'employee'; // Check if user is employee
			isAdmin = userData.user_type === 'admin';
			isCustomer = userData.user_type == 'customer'
		}
		// If employee/Admin, use claimedOrders; otherwise, use pastOrders
		if ((isEmployee || isAdmin) && data.claimedOrders) {
			pastOrders = data.claimedOrders.sort((a, b) => b.id - a.id);
		} else if (data.pastOrders) {
			pastOrders = data.pastOrders.sort((a, b) => b.id - a.id);
		}

		// Shows 3 most recent registered users and 2 most recent active employees
		if (isAdmin && (data as any).recentUsers) {
			recentUsers = (data as any).recentUsers
			.sort((a: any, b: any) => new Date(b.registered_by).getTime() - new Date(a.registered_by).getTime())
			.slice(0, 3);
			console.log('Recent users after sorting and slicing:', recentUsers);

			// Filter from the same array but for only employees, then sort by active_by and take the top two.
			activeEmployees = (data as any).recentUsers
				.filter((user: any) => user.user_type === 'employee')
				.sort((a: any, b: any) => new Date(b.active_by).getTime() - new Date(a.active_by).getTime())
				.slice(0, 2);
			console.log('Active employees after filtering, sorting, slicing:', activeEmployees);
		}

		// Process all orders and take the five most recent ones
		if (isAdmin && (data as any).orders) {
			allRecentOrders = ((data as any).orders as PastOrderType[])
				.sort((a: PastOrderType, b: PastOrderType) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
				.slice(0, 5);
			console.log('Recent orders:', allRecentOrders);
		}

		if (data.error) {
			toastStore.trigger({
				message: data.error,
				background: 'variant-filled-error'
			});
		}
	});

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
			<!-- Additional settings can be added here -->
		</div>


		{#if isAdmin} 
		<!-- this section would have the three most recent registered users, 
		two most recently active employees, and five most recently placed orders -->
		
		<div class="flex flex-col items-center mt-8">
			<h1 class="text-2xl font-semibold">Administrator Dashboard</h1>
			<p class="text-lg text-gray-700">Additional Administrative Information:</p>
			
			<!-- Recently Registered Users -->
			<div class="w-full max-w-lg p-4 border rounded-lg mb-4">
				<h2 class="text-xl font-semibold mb-2">Recently Registered Users</h2>
				{#if recentUsers && recentUsers.length > 0}
					<ul>
						{#each recentUsers as user (user.id)}
							<li class="mb-2">
								<span class="font-bold">{user.name}</span> - {user.email}
							</li>
						{/each}
					</ul>
				{:else}
					<p>No recent users found.</p>
				{/if}
			</div>
			
			<!-- Recently Active Employees -->
			<div class="w-full max-w-lg p-4 border rounded-lg">
				<h2 class="text-xl font-semibold mb-2">Recently Active Employees</h2>
				{#if activeEmployees.length > 0}
					<ul>
						{#each activeEmployees as emp (emp.id)}
							<li class="mb-2">
								<span class="font-bold">{emp.name}</span> - Last Active: {new Date(emp.active_by).toLocaleString()}
							</li>
						{/each}
					</ul>
				{:else}
					<p>No active employees found.</p>
				{/if}
			</div>
			
			<!-- Five Most Recent Orders Section -->
			<div class="w-full max-w-lg p-4 border rounded-lg">
				<h2 class="text-xl font-semibold mb-2">Recently Placed Orders</h2>
				{#if allRecentOrders.length > 0}
				<ul>
					{#each allRecentOrders as order (order.id)}
					<li class="mb-2">
						<span class="font-bold">Order ID: {order.id}</span> – {order.status}<br>
						Placed on: {new Date(order.created_at).toLocaleString()}
					</li>
					{/each}
				</ul>
				{:else}
				<p>No recent orders found.</p>
				{/if}
			</div>
		</div>
		{/if}
		<br>
		<br>

		<!-- Employee/Admin Dashboard Section (for claimed orders) -->
		{#if isEmployee || isAdmin}
		<div class="flex flex-col items-center">
			<h1 class="text-2xl font-semibold">Orders Dashboard</h1>
			<p class="text-lg text-gray-700">Welcome, {userData.name}! You can see your claimed orders here.</p>

			<!-- Display claimed orders -->
			<div class="mt-4 p-4 border border-gray-300 rounded-lg w-full max-w-lg">
				<h2 class="text-xl font-semibold">Claimed Orders</h2>
				<br>
				{#if pastOrders && pastOrders.length > 0}
					<ul>
						{#each pastOrders as order (order.id)}
							<li>
								<a href={`/auth/order-control/expandedOrderView?orderId=${order.id}`} class="order-link">
									<div class="flex flex-col gap-2 items-center card variant-ringed p-4 cursor-pointer">
										<div class="group border rounded-lg p-4 transition-transform duration-300 transform hover:scale-105 cursor-pointer">
											<strong>Order ID:</strong> {order.id} <br>
											<strong>Total:</strong> ${order.total.toFixed(2)} <br>
											<strong>Status:</strong> {order.status} <br>
											<strong>Time Placed:</strong> {new Date(order.created_at).toLocaleString()} <br>
											<strong>Products:</strong>
											<ul class="mt-2">
												{#each order.products as product (product.id)}
													<li class="flex items-center gap-2">
														<ProductSmallPreview product={product} />
														<span class="font-semibold text-black-800">x{product.quantity}</span>
													</li>
												{/each}
											</ul>
										</div>
										<hr class="w-full border-t">
										<p class="text-blue-500 underline">View Details</p>
									</div>
								</a>
							</li>
						{/each}
					</ul>
				{:else}
					<p class="text-center text-lg text-gray-600">No claimed orders yet :/ </p>
					<br>
				{/if}
			</div>
		</div>
		{/if}

		<!-- Past Orders Section for Customers -->
		{#if isCustomer}
		<div class="flex flex-col items-center">
			<h1 class="text-3xl sm:text-4xl md:text-4xl">Past Orders</h1>
            <br>
			{#if pastOrders && pastOrders.length > 0}
				<ul>
					{#each pastOrders as order (order.id)}
						<div class="flex flex-col gap-2 items-center card variant-ringed p-4">
							<li>
								<strong>Order ID:</strong> {order.id} <br>
								<strong>Total:</strong> ${order.total.toFixed(2)} <br>
								<strong>Status:</strong> {order.status} <br>
								<strong>Time Placed:</strong> {new Date(order.created_at).toLocaleString()} <br>
								<strong>Products:</strong>
								<ul class="mt-2">
									{#each order.products as product (product.id)}
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
