<script lang="ts">
  import { onMount } from 'svelte';
  import OrderSmallPreview from '$lib/components/OrderSmallPreview.svelte';
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
  let claimedOrders: PastOrderType[] = [];
  let submitting = false;
  const toastStore = getToastStore();

  onMount(() => {
    userData = data.user;
    unclaimedOrders = data.unclaimedOrders;
    claimedOrders = data.claimedOrders;
  });

  $: {
    console.log('Unclaimed Orders changed:', unclaimedOrders);
  }
  $: {
    console.log('Claimed Orders changed:', claimedOrders);
  }

  async function claimOrder(orderId: number) {
    //If Already Submitting, Exit
    if (submitting) {
      toastStore.trigger({
        message: 'Already Managing Order Claim, Please Wait',
        background: 'variant-filled-error'
      });
      return;
    }

    //Try Submitting
    try {
      submitting = true;
      const formData = new FormData();
      formData.append("order_id", JSON.stringify(orderId));
      formData.append("employee_id", JSON.stringify(userData.id)); 

      // Log the form data entries for debugging
      // for (const [key, value] of formData.entries()) {
      // 	console.log(`${key}: ${value}`);
      // }

      //Post Form Data
      const response = await fetch('?/claimOrder', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      const parsedResultData = JSON.parse(result.data);
      const success = parsedResultData[parsedResultData[0].success];

      if (success) {
        // Success Message
        const successMessage = parsedResultData[parsedResultData[0].message];
        toastStore.trigger({
          message: successMessage,
          background: 'variant-filled-success'
        });

        // Update UI
        const orderToMove = unclaimedOrders.find((o) => o.id === orderId);
        if (orderToMove) {
          unclaimedOrders = unclaimedOrders.filter((o) => o.id !== orderId);
          orderToMove.status = "claimed";
          claimedOrders = [{ ...orderToMove, claimed_by_employee_id: userData.id }, ...claimedOrders];
        }
      }
      else {
        const errorMessage = parsedResultData[parsedResultData[0].error];
        throw new Error(errorMessage);
      }

    } catch (error) {
      const errorMessage: string = `${error}`;
      toastStore.trigger({
        message: errorMessage,
        background: 'variant-filled-error'
      });
    } finally {
      submitting = false;
    }
  }

  async function unclaimOrder(orderId: number) {
    //If Already Submitting, Exit
    if (submitting) {
      toastStore.trigger({
        message: 'Already Managing Order Claim, Please Wait',
        background: 'variant-filled-error'
      });
      return;
    }

    //Try Submitting
    try {
      submitting = true;
      const formData = new FormData();
      formData.append("order_id", JSON.stringify(orderId));

      // Log the form data entries for debugging
      // for (const [key, value] of formData.entries()) {
      // 	console.log(`${key}: ${value}`);
      // }

      //Post Form Data
      const response = await fetch('?/unclaimOrder', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      const parsedResultData = JSON.parse(result.data);
      const success = parsedResultData[parsedResultData[0].success];

      if (success) {
        // Success Message
        const successMessage = parsedResultData[parsedResultData[0].message];
        toastStore.trigger({
          message: successMessage,
          background: 'variant-filled-success'
        });

        // Update UI
        const orderToMove = claimedOrders.find((o) => o.id === orderId);
        if (orderToMove) {
          claimedOrders = claimedOrders.filter((o) => o.id !== orderId);
          orderToMove.status = "pending";
          unclaimedOrders = [{ ...orderToMove, claimed_by_employee_id: undefined }, ...unclaimedOrders];
        }
      }
      else {
        const errorMessage = parsedResultData[parsedResultData[0].error];
        throw new Error(errorMessage);
      }

    } catch (error) {
      const errorMessage: string = `${error}`;
      toastStore.trigger({
        message: errorMessage,
        background: 'variant-filled-error'
      });
    } finally {
      submitting = false;
    }
  }

</script>


<div class="max-w-5xl mx-auto p-6">
  <h1 class="text-center text-4xl font-bold mb-6">Order Control</h1>

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

