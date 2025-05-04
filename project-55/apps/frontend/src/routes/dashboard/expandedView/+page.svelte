<script lang="ts">
    import type { PastOrderType } from '$lib/types/OrderTypes';
    import type { UserType } from '$lib/types/UserTypes';
  
    export let data: {
      user: UserType;
      order: PastOrderType | null;
      error?: string;
    };
  
    const { order, error } = data;
    console.log('[client] customer expandedView data:', data);
  </script>

<div class="max-w-5xl mx-auto p-6">
  {#if error}
    <p class="text-center text-red-500 text-xl font-semibold">{error}</p>
  {:else if order}
    <div class="card variant-surface p-6 space-y-6 shadow-sm transition">
      <!-- Title -->
      <h1 class="text-center text-4xl font-bold">Order Detail: #{order.id}</h1>

      <!-- Summary metrics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="card variant-ghost p-4 text-center">
          <p class="text-sm font-medium text-gray-500">Total</p>
          <p class="mt-1 text-xl font-semibold">${order.total.toFixed(2)}</p>
        </div>
        <div class="card variant-ghost p-4 text-center">
          <p class="text-sm font-medium text-gray-500">Status</p>
          <p class="mt-1 text-xl font-semibold capitalize">{order.status}</p>
        </div>
        <div class="card variant-ghost p-4 text-center">
          <p class="text-sm font-medium text-gray-500">Time Placed</p>
          <p class="mt-1 text-xl font-semibold">
            {new Date(order.created_at).toLocaleString()}
          </p>
        </div>
      </div>

      <!-- Products list -->
      <h2 class="text-2xl font-semibold">Products</h2>
      <ul class="space-y-4">
        {#each order.products as product}
          <li class="card variant-ghost p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <p class="font-semibold text-lg">{product.name}</p>
              {#if product.product_option}
                <p class="mt-1 text-sm text-gray-600">
                  Option: {product.product_option}
                </p>
              {/if}
            </div>
            <div class="flex items-center gap-6 text-sm">
              <span class="font-medium">Qty: {product.quantity}</span>
              <span class="font-medium">Price: ${product.price.toFixed(2)}</span>
            </div>
          </li>
        {/each}
      </ul>

      <!-- Back to orders list -->
      <div class="flex justify-center mt-4">
        <a href="/dashboard" class="btn variant-filled-primary px-6 py-2">
          Back to Dashboard
        </a>
      </div>
    </div>
  {:else}
    <p class="text-center text-gray-500">Loading order details...</p>
  {/if}
</div>
