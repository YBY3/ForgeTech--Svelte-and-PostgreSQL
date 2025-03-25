<script lang="ts">
  import { onMount } from 'svelte';
  import { goto, invalidate } from '$app/navigation';
  import OrderSmallPreview from '$lib/components/OrderSmallPreview.svelte';
  import { getFlaskURL } from '$lib/api';
  import type { PastOrderType } from '$lib/types/OrderTypes';
  import type { UserType } from '$lib/types/UserTypes';

  export let data: {
    user: UserType;
    unclaimedOrders: PastOrderType[];
    claimedOrders: PastOrderType[];
    error?: string;
  };

  let userData: UserType;
  let unclaimedOrders: PastOrderType[] = [];
  let claimedOrders: PastOrderType[] = [];

  onMount(() => {
    userData = data.user;
    unclaimedOrders = data.unclaimedOrders;
    claimedOrders = data.claimedOrders;
  });

// Claim an order
async function claimOrder(orderId: number) {
  try {
    const res = await fetch(`${getFlaskURL()}/api/orders/claim`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: orderId, employee_id: userData.id })
    });
    const result = await res.json();

    if (res.ok && result) {
      // Optionally update the UI immediately
      unclaimedOrders = unclaimedOrders.filter((o) => o.id !== orderId);
      claimedOrders = [result, ...claimedOrders];

      // Force a full page reload
      location.reload();
    } else {
      console.error('Error claiming order:', result.error);
    }
  } catch (error) {
    console.error('Error claiming order:', error);
  }
}

// Unclaim an order
async function unclaimOrder(orderId: number) {
  try {
    const res = await fetch(`${getFlaskURL()}/api/orders/unclaim`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: orderId })
    });
    const result = await res.json();

    if (res.ok && result) {
      // Optionally update the UI immediately
      claimedOrders = claimedOrders.filter((o) => o.id !== orderId);
      unclaimedOrders = [result, ...unclaimedOrders];

      // Force a full page reload
      location.reload();
    } else {
      console.error('Error unclaiming order:', result.error);
    }
  } catch (error) {
    console.error('Error unclaiming order:', error);
  }
}

</script>

<div class="max-w-5xl mx-auto p-6">
  <h1 class="text-center text-4xl font-bold mb-6">Order Dashboard</h1>

  <div class="flex flex-col md:flex-row gap-6">
    <!-- Unclaimed Orders Column -->
    <section class="w-full md:w-1/2">
      <h2 class="text-center text-2xl font-semibold mb-4">Unclaimed Orders</h2>
      {#if unclaimedOrders.length > 0}
        <ul class="space-y-4">
          {#each unclaimedOrders as order (order.id)}
            <li
              class="group border rounded-lg p-4 transition-transform duration-300 transform hover:scale-105 cursor-pointer"
            >
              <div>
                <strong>Order ID:</strong> {order.id} <br />
                <strong>Status:</strong> {order.status} <br />
                <strong>Time Placed:</strong> {new Date(order.created_at).toLocaleString()} 
                <!-- <strong>Total:</strong> $ -->
                <!-- {order.products
                  .reduce((sum, p) => sum + p.price * (p.quantity ?? 1), 0)
                  .toFixed(2)} -->
                <br />
                <strong>Products:</strong>
                <ul class="space-y-2 mt-2">
                  {#each order.products as product}
                    <li>
                      <OrderSmallPreview product={product} orderDisplay={true} />
                    </li>
                  {/each}
                </ul>
              </div>
              <button
                on:click|stopPropagation={() => claimOrder(order.id)}
                class="mt-4 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
              >
                Claim Order
              </button>
            </li>
          {/each}
        </ul>
      {:else}
        <p class="text-center">No unclaimed orders at the moment.</p>
      {/if}
    </section>

    <!-- Claimed Orders Column -->
    <section class="w-full md:w-1/2">
      <h2 class="text-center text-2xl font-semibold mb-4">Claimed Orders</h2>
      {#if claimedOrders.length > 0}
        <ul class="space-y-4">
          {#each claimedOrders as order (order.id)}
            <li
              class="group border rounded-lg p-4 transition-transform duration-300 transform hover:scale-105 cursor-pointer"
            >
              <div>
                <strong>Order ID:</strong> {order.id} <br />
                <strong>Status:</strong> {order.status} <br />
                <!-- <strong>Claimed By:</strong> {order.claimed_by_employee_id} <br /> -->
                <strong>Time Placed:</strong> {new Date(order.created_at).toLocaleString()} 
                <!-- <strong>Total:</strong> $ -->
                <!-- {order.products
                  .reduce((sum, p) => sum + p.price * (p.quantity ?? 1), 0)
                  .toFixed(2)} -->
                <br />
                <strong>Products:</strong>
                <ul class="space-y-2 mt-2">
                  {#each order.products as product}
                    <li>
                      <OrderSmallPreview product={product} orderDisplay={true} />
                    </li>
                  {/each}
                </ul>
              </div>
              <button
                on:click|stopPropagation={() => unclaimOrder(order.id)}
                class="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
              >
                Unclaim Order
              </button>
            </li>
          {/each}
        </ul>
      {:else}
        <p class="text-center">No claimed orders yet.</p>
      {/if}
    </section>
  </div>
</div>

