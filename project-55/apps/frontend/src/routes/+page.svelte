<script lang="ts">
    import { productStore, selectedProduct } from "$lib/stores/orders"; 
    import type { Product } from "$lib/stores/orders"; // Import Product type
    import { writable } from "svelte/store";

    // Temporary placeholder product
    const tempProduct: Product = {
		name: "GeForce RTX 4090",
		image: "/LandingPage-pic/4090.jpg", // Replace with actual path
		price: 499.99,
		description: "High-performance graphics card for gaming and content creation.",
		components: ["8GB GDDR6 Memory", "Ray Tracing Support", "PCIe 4.0"],
		id: 0
	};

    // Use $productStore to access store reactively
    let products = $productStore;
    function selectProduct(product: Product) {  // Explicitly type 'product'
      selectedProduct.set(product);
    }

     // Reactive store to control alert visibility
     let visible = writable(false);
     let message = writable("Login functionality coming soon!"); // Message to be displayed
     let title = writable("Notice"); // Title for the alert

     // Function to handle login
    function handleLogin() {
        // Show the alert with the message when login is clicked
        visible.set(true);
    }
    // import { productStore } from "$lib/StoreOrders/orders"; 
    import { addToOrder } from "$lib/stores/orders"; 
  </script>
  
  <main class="h-full bg-background flex flex-col items-center overflow-y-auto">
    
    <!-- Header -->
    <header class="bg-surface-700 text-on-surface p-4 w-full flex flex-col items-center justify-center min-h-[40vh]">
        <img src="/LandingPage-pic/logo.png" class="w-85 h-auto" />
    </header>
  
    <!-- Main Content -->
    <br><h1 class="text-4xl font-bold text-white">Featured Item</h1>
    <div class="container mx-auto p-4 flex flex-col items-center text-center">
        {#if $selectedProduct}
            <!-- Featured Product -->
            <div class="bg-gray-800 text-white p-6 rounded-lg shadow-md w-96">
                <h2 class="text-2xl font-semibold text-white-900">{$selectedProduct.name}</h2>
                <img src="{$selectedProduct.image}" alt="{$selectedProduct.name}" class="max-w-full h-auto rounded-lg shadow-md mt-3" />
                <p class="text-red-500 mt-2">{$selectedProduct.description}</p>
                <p class="text-lg font-bold mt-1 text-green-600">${$selectedProduct.price}</p>
                <h3 class="text-xl font-semibold mt-2 text-white-800">Components:</h3>
                <ul class="list-disc list-inside text-white-700">
                    {#each $selectedProduct.components as component}
                        <li>{component}</li>
                    {/each}
                </ul>
            </div>
        {:else}
            <!-- Temporary Product Display -->
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div class="bg-gray-800 text-white p-6 rounded-lg shadow-md w-96" 
                 on:click={() => selectProduct(tempProduct)}>
                <img src="{tempProduct.image}" alt="{tempProduct.name}" class="w-full h-auto rounded-md" />
                <h2 class="text-xl font-bold mt-2">{tempProduct.name}</h2>
                <p class="text-gray-600">${tempProduct.price}</p>
                <p class="text-red-700 underline">Click to view details</p>
            </div>

        {/if}
        
        <!-- Alert Message -->
        {#if $visible}
            <aside class="alert variant-ghost p-4 rounded-md shadow-md mb-4 bg-yellow-200">
                <!-- Icon -->
                <div class="icon">
                    <!-- You can replace this with an actual icon if needed -->
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>

                <!-- Message -->
                <div class="alert-message">
                    <h3 class="h3 font-semibold text-red-700">{ $title }</h3>
                    <p>{ $message }</p>
                </div>

                <!-- Actions -->
                <div class="alert-actions">
                    <!-- Add button(s) or action(s) here if necessary -->
                    <button on:click={() => visible.set(false)} class="bg-red-700 text-white px-4 py-2 rounded-md mt-2">
                        Close
                    </button>
                </div>
            </aside>
        {/if}

        <!-- Buttons & Cart Display -->
        <br>
        <div class="flex items-center space-x-4">
            <button on:click={handleLogin} class="bg-gray-800 text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-600 transition">
                Login
            </button>
            <button disabled class="bg-gray-800 text-white px-4 py-2 rounded-lg shadow-md opacity-50 cursor-not-allowed">
                Add to Cart
            </button>
            <span class="bg-gray-300 text-gray-800 px-3 py-1 rounded-full shadow-md text-lg font-semibold">
                0
            </span>
        </div>
        <div class="container mx-auto p-4 flex flex-col items-center text-center pb-20"></div>

        <!-- About Us -->
        <h1 class="text-4xl font-bold text-white">About The Company</h1> <br>
        <div class="bg-gray-800 text-white p-6 rounded-lg shadow-md w-full max-w-4xl">
            <p class="text-white-700">We are a group of college students with a 
            passion for technology, dedicated to providing high-quality 
            computer parts for both new and old systems. Whether you're 
            building a custom rig or upgrading your current setup, we 
            offer a wide range of components—ranging from the latest hardware 
            to reliable, refurbished parts. Our mission is to make technology 
            more accessible, affordable, and sustainable, all while supporting 
            the growth of young entrepreneurs. Join us in shaping the future, 
            one part at a time!
            </p>
        </div> <br>


    </div>
  </main>