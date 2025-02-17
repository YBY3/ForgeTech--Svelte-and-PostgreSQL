<script lang="ts">
    import { productsStore } from "$lib/stores/ProductsStore";
    import type { ProductType } from "$lib/types/ProductTypes"
    import '@fortawesome/fontawesome-free/css/all.min.css';
    // These variables are only used locally, no need for writeable 
    let featuredProduct: ProductType = $productsStore[0]
    let visible = false;
    let message = "Login functionality coming soon!"; 
    let title = "Notice"; 

     // Function to handle login
    function handleLogin() {
        // Show the alert with the message when login is clicked
        visible = true;
    }
  </script>

  
  <!-- this is being rendered as a component to the layout, use div instead of main for best practice -->
  <div class="h-full bg-background flex flex-col items-center overflow-y-auto scroll-smooth">
    
    <div class="relative w-full h-full"> 
    <img class="absolute top-0 left-0 w-full h-full object-contain object-[85%] z-[-1] hidden xl:block" src="LandingPage-pic/gpu.png" alt="GPU Image">
    <div class="z-[-2] absolute top-[47%] left-[70%] -translate-x-1/2 -translate-y-1/2 w-[30rem] h-[30rem] bg-primary-500 rounded-full blur-3xl opacity-30 animate-pulse hidden xl:block"></div>


    <div class="items-center space-x-4 sm:space-x-6 md:space-x-8 w-full space-y-2 px-0 md:px-16 xl:px-32 mt-8 md:mt-32 mb-32">
        <img src="LandingPage-pic/Logo Icon.png" class="w-24 sm:w-24 md:w-32">
        <h1 class="text-4xl sm:text-4xl md:text-6xl font-bold">
            <span class="text-primary-500">Forge</span> power.
        </h1>
        <h1 class="text-4xl sm:text-4xl md:text-6xl font-bold">
            <span class="text-primary-500">Fuel</span> performance.
        </h1>
        
        <p class="text-base md:text-lg max-w-xs sm:max-w-sm md:max-w-lg">
            Whether you're building a custom rig or upgrading your current setup,
            we offer a wide range of components—ranging from the latest hardware to
            reliable, refurbished parts.
        </p>
        
        <div class="flex space-x-4 mt-6">
            <a href="/catalog"><button type="button" class="btn border-2 border-primary-500 text-white rounded-lg bg-primary-500 px-8 py-3 hover: transition-all duration-300 ease-in-out hover:shadow-[0_0_20px_5px_rgba(212,22,60,0.7)]">
                Shop <i class="fa-solid fa-arrow-right ml-1"></i>
            </button></a>
            <button type="button" class="btn rounded-lg border-2 border-white px-8 py-3 hover:bg-white transition-all duration-300 ease-in-out hover:text-black">
                Learn More 
            </button>
        </div>
    </div>
    </div>

<div class="sticky top-0 w-full variant-glass-surface text-center flex justify-evenly py-6 z-[2]">
    <button class="border-b-4 border-primary-500 border-opacity-0 hover:border-opacity-100 transition-all duration-300 ease-in-out"><a href="#products">PRODUCTS</a></button>
    <button class="border-b-4 border-primary-500 border-opacity-0 hover:border-opacity-100 transition-all duration-300 ease-in-out"><a href="#partnersID">PARTNERS</a></button>
    <button class="border-b-4 border-primary-500 border-opacity-0 hover:border-opacity-100 transition-all duration-300 ease-in-out"><a href="#AboutID">CONTACT</a></button>
    <button class="border-b-4 border-primary-500 border-opacity-0 hover:border-opacity-100 transition-all duration-300 ease-in-out"><a href="#AboutID">ABOUT</a></button>
</div>
    
    <!-- Main Content -->
    <br><h1 class="text-4xl font-bold" id="products">Featured Product</h1>
    <div class="container mx-auto p-4 flex flex-col items-center text-center">
        {#if featuredProduct}
            <!-- Featured Product -->
            <div class="bg-gray-800 text-white p-6 rounded-lg shadow-md w-96">
                <h2 class="text-2xl font-semibold text-white-900">{featuredProduct.name}</h2>
                <!-- The image is not working right now in the backend, will fix this later -->
                <!-- <img src="{featuredProduct.image}" alt="{featuredProduct.name}" class="max-w-full h-auto rounded-lg shadow-md mt-3" /> -->
                <p class="text-red-500 mt-2">{featuredProduct.description}</p>
                <p class="text-lg font-bold mt-1 text-green-600">${featuredProduct.price}</p>
                <h3 class="text-xl font-semibold mt-2 text-white-800">Components:</h3>
                <ul class="list-disc list-inside text-white-700">
                    {#each featuredProduct.components as component}
                        <li>{component}</li>
                    {/each}
                </ul>
            </div>
        {:else}
            <!-- Instead of Temperary Product, Use a Error Message -->
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

<h1 class="text-4xl font-bold" id="partnersID">Partners</h1>
<br>
<div class="logo-cloud grid-cols-2 sm:grid-cols-4 md:grid-cols-4 xl:grid-cols-4 2xl:grid-cols-4 gap-0.5">
	<a class="logo-item p-8 text-xl">AMD</a>
	<a class="logo-item p-8 text-xl">Nvidia</a>
	<a class="logo-item p-8 text-xl">Intel</a>
	<a class="logo-item p-8 text-xl">Qualcomm</a>
	<a class="logo-item p-8 text-xl">Stark Industries</a>
	<a class="logo-item p-8 text-xl">Samsung</a>
	<a class="logo-item p-8 text-xl">ZOTAC</a>
	<a class="logo-item p-8 text-xl">Wonka Inc.</a>
</div>
<br>
<br>

        <!-- About Us -->
        <h1 class="text-4xl font-bold" id="AboutID">About The Company</h1> <br>
        <div class="bg-surface-100 dark:bg-surface-800 p-6 rounded-lg shadow-md w-full max-w-4xl">
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
</div>