<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import OrderSmallPreview from '$lib/components/OrderSmallPreview.svelte';

  // Define product and order types
  type Product = {
    id: number;
    name: string;
    description: string;
    price: number;
    quantity?: number;
  };

  type OrderType = {
    id: number;
    createdAt: Date;
    status: string;
    products: Product[];
    claimedBy?: string;
  };

  // Hard-coded unclaimed orders data
  let unclaimedOrders: OrderType[] = [
    {
      id: 1,
      createdAt: new Date('2023-01-01T10:00:00Z'),
      status: 'Pending',
      products: [
        { id: 101, name: "Laptop", description: "Sample Laptop", price: 999.99, quantity: 2 },
        { id: 102, name: "Mouse", description: "Wireless Mouse", price: 49.99, quantity: 1 }
      ]
    },
    {
      id: 2,
      createdAt: new Date('2023-01-02T10:00:00Z'),
      status: 'Pending',
      products: [
        { id: 103, name: "Keyboard", description: "Mechanical Keyboard", price: 79.99, quantity: 1 }
      ]
    },
    {
      id: 3,
      createdAt: new Date('2023-01-03T10:00:00Z'),
      status: 'Pending',
      products: [
        { id: 104, name: "Monitor", description: "27-inch Monitor", price: 299.99, quantity: 1 },
        { id: 105, name: "USB Hub", description: "4-Port USB Hub", price: 29.99, quantity: 3 }
      ]
    }
  ];

  // Initially, claimed orders are empty
  let claimedOrders: OrderType[] = [];

  // Simulated logged-in employee
  let currentEmployee = { firstName: "Test", lastName: "Employee" };

  // Function to claim an order
  function claimOrder(orderId: number) {
    const index = unclaimedOrders.findIndex(order => order.id === orderId);
    if (index !== -1) {
      const order = unclaimedOrders[index];
      order.status = 'Claimed';
      order.claimedBy = `${currentEmployee.firstName} ${currentEmployee.lastName}`;
      unclaimedOrders = unclaimedOrders.filter(o => o.id !== orderId);
      claimedOrders = [ ...claimedOrders, order ];
    }
  }

  // Function to unclaim an order
  function unclaimOrder(orderId: number) {
    const index = claimedOrders.findIndex(order => order.id === orderId);
    if (index !== -1) {
      const order = claimedOrders[index];
      order.status = 'Pending';
      delete order.claimedBy;
      claimedOrders = claimedOrders.filter(o => o.id !== orderId);
      unclaimedOrders = [ ...unclaimedOrders, order ];
    }
  }

  // Reactive statement to sort unclaimed orders (oldest first)
  $: sortedUnclaimedOrders = [...unclaimedOrders].sort(
    (a, b) => a.createdAt.getTime() - b.createdAt.getTime()
  );

  // Function to navigate to the expanded order view.
  function viewOrder(orderId: number) {
    goto(`/orders/${orderId}`);
  }
</script>

<div class="max-w-5xl mx-auto p-6">
  <h1 class="text-center text-4xl font-bold mb-6">Order Dashboard</h1>

  <!-- Flex container for side-by-side layout on medium screens and up -->
  <div class="flex flex-col md:flex-row gap-6">
    <!-- Unclaimed Orders Column -->
    <section class="w-full md:w-1/2">
      <h2 class="text-center text-2xl font-semibold mb-4">Unclaimed Orders</h2>
      {#if sortedUnclaimedOrders.length > 0}
        <ul class="space-y-4">
          {#each sortedUnclaimedOrders as order (order.id)}
            <li class="group border rounded-lg p-4 transition-transform duration-300 transform hover:scale-105 cursor-pointer"
                on:click={() => viewOrder(order.id)}>
              <div>
                <strong>Order ID:</strong> {order.id} <br>
                <strong>Status:</strong> {order.status} <br>
                <strong>Time Placed:</strong> {order.createdAt.toLocaleString()} <br>
                <strong>Total:</strong> ${order.products.reduce((sum, p) => sum + p.price * (p.quantity ?? 1), 0).toFixed(2)} <br>
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
            <li class="group border rounded-lg p-4 transition-transform duration-300 transform hover:scale-105 cursor-pointer"
                on:click={() => viewOrder(order.id)}>
              <div>
                <strong>Order ID:</strong> {order.id} <br>
                <strong>Status:</strong> {order.status} <br>
                <strong>Claimed By:</strong> {order.claimedBy} <br>
                <strong>Time Placed:</strong> {order.createdAt.toLocaleString()} <br>
                <strong>Total:</strong> ${order.products.reduce((sum, p) => sum + p.price * (p.quantity ?? 1), 0).toFixed(2)} <br>
                <strong>Products:</strong>
                <ul class="space-y-2 mt-2">
                  {#each order.products as product}
                    <li>
                      <OrderSmallPreview product={product} orderDisplay={true} />
                    </li>
                  {/each}
                </ul>
              </div>
              <!-- Unclaim Order Button -->
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
  
  <!-- Commented space for future Expanded Order View Component -->
  <!-- {
    TODO: When the expanded order view component is ready,
    integrate it on the route /orders/[orderId] to display detailed information.
  } -->
</div>

