<script lang="ts">
    import { onMount } from 'svelte';
    import type { ProductType } from "$lib/types/ProductTypes"
    import { addToOrder } from "$lib/stores/OrdersStore";
	import { productsStore } from '$lib/stores/ProductsStore.js';
	import ProductCard from '$lib/components/product/ProductCard.svelte';
	import { goto } from '$app/navigation';
    

    //Data
    export let data;
    let featuredProduct: ProductType;
    let isLoggedIn = false;

    // These variables are only used locally, no need for writeable 
    let visible = false;
    let message = "Login functionality coming soon!"; 
    let title = "Notice"; 

    let productData: ProductType[];
    const ALLProducts = productsStore;

    onMount(() => {
        if (data.products) {
            featuredProduct = data.products.find(p => p.name.includes("3090")) ?? data.products[0];
        }
        if (data.isLoggedIn) {
            isLoggedIn = data.isLoggedIn;
        }

        if (data.products) {
      productData = data.products;
      productsStore.set(productData);
    }
    });

  </script>

  
  <!-- this is being rendered as a component to the layout, use div instead of main for best practice -->
  <div class="h-full bg-background flex flex-col items-center overflow-y-auto overflow-x-hidden scroll-smooth">
    
    <div class="relative w-full h-full"> 
    <img 
        class="absolute top-0 left-0 w-full h-full object-contain object-[85%] z-[-1] hidden xl:block" 
        src="misc/gpu.png" 
        alt="Sample GPU"
    >
    <div class="z-[-2] absolute top-[47%] left-[70%] -translate-x-1/2 -translate-y-1/2 w-[30rem] h-[30rem] bg-primary-500 rounded-full blur-3xl opacity-30 animate-pulse hidden xl:block"></div>


    <div class="flex flex-col items-center md:text-left md:items-start space-x-4 sm:space-x-6 md:space-x-8 space-y-2 px-0 md:px-16 xl:px-32 mt-8 md:mt-32 mb-32">
        <img 
            class="w-24 sm:w-24 md:w-32" 
            src="forgetech_logos/small.png" 
            alt="ForgeTech Logo"
        >
        <h1 class="[@media(max-width:430px)]:text-3xl text-5xl sm:text-6xl md:text-6xl font-bold">
            <span class="text-primary-500">Forge</span> power.
        </h1>
        <h1 class="[@media(max-width:430px)]:text-3xl text-5xl sm:text-6xl md:text-6xl font-bold">
            <span class="text-primary-500">Fuel</span> performance.
        </h1>
        
        <p class="text-base text-center md:text-left md:text-lg max-w-xs sm:max-w-sm md:max-w-lg">
            Whether you're building a custom rig or upgrading your current setup,
            we offer a wide range of components—ranging from the latest hardware to
            reliable, refurbished parts.
        </p>
        
        <div class="flex space-x-4 mt-6">
            <a href="/catalog"><button type="button" class="btn border-2 border-primary-500 text-white rounded-lg bg-primary-500 px-8 py-3 hover: transition-all duration-300 ease-in-out hover:shadow-[0_0_20px_5px_rgba(212,22,60,0.7)]">
                Shop <i class="fa-solid fa-arrow-right ml-1"></i>
            </button></a>
            <a href="#second_tab"><button type="button" class="btn rounded-lg border-2 border-white px-8 py-3 hover:bg-white transition-all duration-300 ease-in-out hover:text-black">
                Learn More 
            </button></a>
        </div>
    </div>
    </div>

<div class="sticky top-0 w-full bg-surface-200 dark:bg-surface-700 md:text-center md:flex md:justify-evenly py-6 z-[2]" id="second_tab">
    <!--<button class="border-b-4 border-primary-500 border-opacity-0 hover:border-opacity-100 transition-all duration-300 ease-in-out block md:hidden px-8"><a href="#products">PRODUCTS</a></button>-->
    <select class="select w-32 block md:hidden ml-4">
        <option value="1">Featured</option>
        <option value="2">Partners</option>
        <option value="3">Contact</option>
        <option value="4">About</option>
    </select>
    <button class="border-b-4 border-primary-500 border-opacity-0 hover:border-opacity-100 transition-all duration-300 ease-in-out hidden md:block"><a href="#products">FEATURED</a></button>
    <button class="border-b-4 border-primary-500 border-opacity-0 hover:border-opacity-100 transition-all duration-300 ease-in-out hidden md:block"><a href="#partnersID">PARTNERS</a></button>
    <button class="border-b-4 border-primary-500 border-opacity-0 hover:border-opacity-100 transition-all duration-300 ease-in-out hidden md:block"><a href="#AboutID">CONTACT</a></button>
    <button class="border-b-4 border-primary-500 border-opacity-0 hover:border-opacity-100 transition-all duration-300 ease-in-out hidden md:block"><a href="#AboutID">ABOUT</a></button>
</div>
    
    <!-- Main Content -->
    <!--<h1 class="text-4xl font-bold" id="products">Featured</h1> p-4 was below!-->
    <div class="container mx-auto flex flex-col items-center">
        {#if featuredProduct}
            <div id="products" class="bg-black w-screen">
                <br>
                <h2 class="text-2xl font-semibold text-white-900 font-bold text-center text-white">{featuredProduct.name}</h2>
                <br>
                <h1 class="text-2xl sm:text-4xl font-bold text-center text-white">Unleash powerful graphics for gamers and creators.</h1> 
                <br>
                <div class="flex lg:flex-row flex-col items-center justify-center gap-x-6">
                    <div class="w-full lg:w-1/2 [@media(min-width:2000px)]:ml-32 [@media(min-width:2400px)]:ml-96">
                    <img 
                    class="rounded-lg"
                    src={featuredProduct.image_urls[0]}
                    alt="NVIDIA GeForce RTX 3090 Ti"
                    />
                    </div>
                    <div class="flex-1 p-6 rounded-lg w-full [@media(min-width:2000px)]:-ml-32 [@media(min-width:2400px)]:-ml-64 text-white">
                        <!-- The image is not working right now in the backend, will fix this later -->
                        <!-- <img src="{featuredProduct.image}" alt="{featuredProduct.name}" class="max-w-full h-auto rounded-lg shadow-md mt-3" /> -->
                        <p class="mt-2"><span class="text-primary-500 text-3xl font-bold">Unmatched Performance</span><br>
                            Experience smooth, lifelike visuals with cutting-edge ray tracing technology.</p>
                        <br>
                        <p class="mt-2"><span class="text-primary-500 text-3xl font-bold">Effortless Rendering</span><br>
                            Seamlessly bring your world to life with unmatched graphics power and optimization.</p>
                        <br>
                        <p class="mt-2"><span class="text-primary-500 text-3xl font-bold">Gaming at the Edge</span><br>
                            Elevate your experience with blazing-fast cores and AI-driven performance.</p>
                        <!--<br>
                        <p class="mt-2"><br>
                            {featuredProduct.description}</p>-->
                        <br>
                        <div class="flex gap-2 items-center">
                            <div class="border-2 border-white py-2 px-6 rounded-lg inline-block"><p class="text-lg font-bold">${featuredProduct.price}</p></div>

                            <!-- Shopping Cart Button -->
                            <a class="relative group" href="/orders" >
                                <button 
                                class="w-12 h-12 border border-2 border-black dark:border-white rounded-md flex items-center justify-center hover:bg-primary-500 transition hover:border-none hover:shadow-[0_0_20px_5px_rgba(212,22,60,0.7)] disabled:opacity-50 disabled:cursor-not-allowed"
                                disabled={!isLoggedIn}
                                on:click={() => addToOrder(featuredProduct)}
                                >
                                <i class="fa-solid fa-cart-shopping"></i>
                                </button>
                                
                                <!-- Tooltip Below -->
                                <span class="absolute left-1/2 -translate-x-1/2 translate-y-1/3 bg-black text-white text-sm px-3 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                                {#if isLoggedIn}
                                    Add to Cart
                                {:else}
                                    Login 
                                {/if}
                                </span>
                            </a>
                        </div>
                        <!--<h3 class="text-xl font-semibold mt-2 text-white-800">Components:</h3>

                        <ul class="list-disc list-inside text-white-700">
                            {#each featuredProduct.components as component}
                                <li>{component}</li>
                            {/each}
                        </ul>-->
                    </div>
                </div>
            </div>
        {:else}
             <br>
            <div class="w-auto h-auto card variant-ghost-error rounded-lg p-4">
                <div class="text-2xl font-bold">The Product Information Failed to Load :/</div>
                <div class="text-xl">if refreshing fails, we are working on fix</div>
            </div>
        {/if}
        
        <!-- Alert Message -->
        {#if visible}
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
                    <h3 class="h3 font-semibold text-red-700">{ title }</h3>
                    <p>{ message }</p>
                </div>

                <!-- Actions -->
                <div class="alert-actions">
                    <!-- Add button(s) or action(s) here if necessary -->
                    <button on:click={() => visible = false} class="bg-red-700 text-white px-4 py-2 rounded-md mt-2">
                        Close
                    </button>
                </div>
            </aside>
        {/if}
        
        <!-- we want this for logged in users only, would consider removing this logic -->
        <!-- Buttons & Cart Display -->
        <!--<div class="container mx-auto p-4 flex flex-col items-center text-center pb-20"></div>-->
<div class="bg-white dark:bg-black w-screen">
<br>
<br>
<br>
<h2 class="text-2xl font-semibold text-white-900 font-bold text-center">Discover a Few of Our Favorites</h2>
<br>
<h1 class="text-2xl sm:text-4xl font-bold text-center">Reliable. Powerful. Ready to perform.</h1> 
<br>
    <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-6">
        {#each $ALLProducts.slice(0, 4) as product}
          <ProductCard 
          product={product} 
          onProductSelect={(product) => goto(`/products/${product.id}`)} 
          isLoggedIn={isLoggedIn}
          />
        {/each}
      </div>  
<br>
<br>
<br>
</div>

<div class="bg-white w-screen items-center" id="partnersID">
    <br>
<br>
<br>
<h2 class="text-2xl text-black font-semibold text-white-900 font-bold text-center">Trusted by Top Brands</h2>
<br>
<h1 class="text-2xl text-black sm:text-4xl font-bold text-center">Partners powering every build.</h1> 

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 items-center ml-8 sm:ml-10">
    <div class="w-64"><img src="brands/nvidia.webp" alt="nvidia Logo"></div>
    <div class="w-64"><img src="brands/evga.png" alt="evga Logo"></div>
    <div class="w-64"><img src="brands/amd.webp" alt="amd Logo"></div>
    <div class="w-64"><img src="brands/msi.png" alt="msi Logo"></div>
    <div class="w-64"><img src="brands/gigabyte.png" alt="gigabyte Logo"></div>
    <div class="w-64"><img src="brands/intel.png" alt="intel Logo"></div>
    </div>
    <br>
<br>
<br>
</div>

        <!-- About Us -->
        <div class="lg:py-16 bg-primary-500 w-screen flex flex-col lg:flex-row items-center lg:items-start justify-center gap-8">
        
        <div class="p-6 px-4 rounded-lg w-full max-w-xl">
            <h1 class="text-4xl font-bold text-white [@media(max-width:430px)]:text-3xl text-4xl sm:text-6xl md:text-6xl" id="AboutID">About Forge Tech</h1> <br>
            <p class="text-gray-200 text-sm sm:text-lg">We are a group of college students with a 
            passion for technology, dedicated to providing high-quality 
            computer parts for both new and old systems. Whether you're 
            building a custom rig or upgrading your current setup, we 
            offer a wide range of components—ranging from the latest hardware 
            to reliable, refurbished parts. Our mission is to make technology 
            more accessible, affordable, and sustainable, all while supporting 
            the growth of young entrepreneurs. Join us in shaping the future, 
            one part at a time!
            </p>
            <br>
            <a href="/about-us"><button class="text-black font-bold p-2 border-2 border-black rounded-lg hover:bg-white transition-all duration-300 ease-in-out hover:border-white">Meet the Team <i class="fa-solid fa-arrow-right ml-1"></i></button></a>
            <a href="/about-us"><button class="text-black font-bold p-2 border-2 border-black rounded-lg hover:bg-white transition-all duration-300 ease-in-out hover:border-white">Contact Us <i class="fa-solid fa-arrow-right ml-1"></i></button></a>
        </div> 
        
            <div class="p-2">
            <img 
                class ="w-96 rounded-full"
                src="leo-pics/leo-cropped.png"
                alt="LEO"
            >
            </div>

        </div>

    </div>
</div>