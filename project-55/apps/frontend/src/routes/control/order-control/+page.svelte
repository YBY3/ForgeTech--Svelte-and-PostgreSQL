<!-- src/routes/control/order-control/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import OrderControlCard from '$lib/components/control/OrderControlCard.svelte';
	import type { PastOrderType } from '$lib/types/OrderTypes';
	import type { UserType } from '$lib/types/UserTypes';
	import { getToastStore } from '@skeletonlabs/skeleton';

	export let data: {
		user: UserType;
		unclaimedOrders: PastOrderType[];
		claimedOrders: PastOrderType[];
		error?: string;
	};

	let userData: UserType;
	let unclaimedOrders: PastOrderType[] = [];
	let claimedOrders: PastOrderType[]   = [];
	let submitting = false;
	const toastStore = getToastStore();

	onMount(() => {
		userData = data.user;
		unclaimedOrders = data.unclaimedOrders
			.slice()
			.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
		claimedOrders = data.claimedOrders
			.slice()
			.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
	});

	async function claimOrder(orderId: number) {
		if (submitting) {
			toastStore.trigger({
				message: 'Already managing order claim—please wait',
				background: 'variant-filled-error'
			});
			return;
		}

		try {
			submitting = true;
			const formData = new FormData();
			formData.append('order_id', JSON.stringify(orderId));
			formData.append('employee_id', JSON.stringify(userData.id));

			const response = await fetch('?/claimOrder', { method: 'POST', body: formData });
			const result = await response.json();
			const parsedResultData = JSON.parse(result.data);

			// old‑style lookup: first element tells you where to find success/message/error
			const success = parsedResultData[ parsedResultData[0].success ];
			if (success) {
				const successMessage = parsedResultData[ parsedResultData[0].message ];
				toastStore.trigger({
					message: successMessage,
					background: 'variant-filled-success'
				});

				const orderToMove = unclaimedOrders.find(o => o.id === orderId);
				if (orderToMove) {
					unclaimedOrders = unclaimedOrders.filter(o => o.id !== orderId);
					orderToMove.status = 'claimed';
					claimedOrders = [
						{ ...orderToMove, claimed_by_employee_id: userData.id },
						...claimedOrders
					];
				}
			} else {
				const errorMessage = parsedResultData[ parsedResultData[0].error ];
				throw new Error(errorMessage);
			}
		} catch (err) {
			toastStore.trigger({
				message: `${err}`,
				background: 'variant-filled-error'
			});
		} finally {
			submitting = false;
		}
	}

	async function unclaimOrder(orderId: number) {
		if (submitting) {
			toastStore.trigger({
				message: 'Already managing order unclaim—please wait',
				background: 'variant-filled-error'
			});
			return;
		}

		try {
			submitting = true;
			const formData = new FormData();
			formData.append('order_id', JSON.stringify(orderId));

			const response = await fetch('?/unclaimOrder', { method: 'POST', body: formData });
			const result = await response.json();
			const parsedResultData = JSON.parse(result.data);

			const success = parsedResultData[ parsedResultData[0].success ];
			if (success) {
				const successMessage = parsedResultData[ parsedResultData[0].message ];
				toastStore.trigger({
					message: successMessage,
					background: 'variant-filled-success'
				});

				const orderToMove = claimedOrders.find(o => o.id === orderId);
				if (orderToMove) {
					claimedOrders = claimedOrders.filter(o => o.id !== orderId);
					orderToMove.status = 'pending';
					unclaimedOrders = [
						{ ...orderToMove, claimed_by_employee_id: undefined },
						...unclaimedOrders
					];
				}
			} else {
				const errorMessage = parsedResultData[ parsedResultData[0].error ];
				throw new Error(errorMessage);
			}
		} catch (err) {
			toastStore.trigger({
				message: `${err}`,
				background: 'variant-filled-error'
			});
		} finally {
			submitting = false;
		}
	}
</script>

<div class="max-w-5xl mx-auto p-6 space-y-8">
	<h1 class="text-center text-4xl font-bold">Order Control</h1>

	<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
		<!-- Unclaimed -->
		<section>
			<h2 class="text-2xl font-semibold mb-4 text-center">Unclaimed Orders</h2>
			{#if unclaimedOrders.length > 0}
			<ul class="space-y-4">
				{#each unclaimedOrders as order (order.id)}
				  <li
					class="border border-gray-300 rounded-lg p-4 flex flex-col gap-4
						   transform hover:scale-105 transition-transform duration-300 ease-in-out"
				  >
					  <OrderControlCard {order} />
				
					<div class="flex justify-center">
					  <button
						on:click|stopPropagation={() => claimOrder(order.id)}
						class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
					  >
						Claim Order
					  </button>
					</div>
				  </li>
				{/each}
			  </ul>			  
			{:else}
				<p class="text-center">No unclaimed orders at the moment.</p>
			{/if}
		</section>

		<!-- Claimed -->
		<section>
			<h2 class="text-2xl font-semibold mb-4 text-center">Claimed Orders</h2>
			{#if claimedOrders.length > 0}
			<ul class="space-y-4">
				{#each claimedOrders as order (order.id)}
				  <li
					class="border border-gray-300 rounded-lg p-4 flex flex-col gap-4
						   transform hover:scale-105 transition-transform duration-300 ease-in-out"
				  >
					<a
					  href={`/control/order-control/expandedOrderView?orderId=${order.id}`}
					  class="block"
					>
					  <OrderControlCard {order} />
					</a>
					<div class="flex justify-center">
					  <button
						on:click|stopPropagation={() => unclaimOrder(order.id)}
						class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
					  >
						Unclaim Order
					  </button>
					</div>
				  </li>
				{/each}
			  </ul>			  
			{:else}
				<p class="text-center">No claimed orders yet.</p>
			{/if}
		</section>
	</div>
</div>
