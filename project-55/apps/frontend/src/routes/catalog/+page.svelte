<script lang="ts">
    import { productsStore } from "$lib/stores/ProductsStore"; 
    import { addToOrder } from "$lib/stores/OrdersStore"; 
    import type { ProductType } from "$lib/types/ProductTypes"

    let selectedProduct: ProductType;
    let catalogView = true;
    let productView = false;

    function showCatalogView() {
        productView = false;
        catalogView = true;
    }

    function showProductView() {
        catalogView = false;
        productView = true;
    }
</script>


{#if catalogView}
    
    <div class="flex flex-col items-center w-full h-full overflow-y-auto">
        <br>
        <h1 class="text-center text-4xl font-medium">Our Products</h1>
        <br>

        <!-- Catalog Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6">
            {#each $productsStore as product}
                <div class="relative card variant-filled-primary card-hover rounded-lg shadow-md p-4">

                    <!-- Make Image Clickable -->
                    <button 
                        class="w-full h-60 flex items-center justify-center bg-gray-200"
                        on:click={() => {
                            selectedProduct = product
                            showProductView()
                        }}
                    >
                        <!-- The image is not working right now in the backend, will fix this later -->
                        <!-- <img 
                        class="max-h-full max-w-full object-contain rounded-md cursor-pointer" 
                        src={product.image} 
                        alt={product.name}
                        /> -->
                    </button>  

                    <br>

                    <h2 class="text-lg font-semibold text-black-800">{product.name}</h2>
                    <p class="text-black-600 text-sm">{product.description}</p>
                    <!-- Price & Cart Button Section -->
                    <div class="flex justify-between items-center mt-4">
                        <p class="text-lg font-semibold text-gray-900">${product.price.toFixed(2)}</p>

                        <!-- Add to Cart Button with Tooltip -->
                        <div class="relative group">
                            <button 
                                class="w-10 h-10 bg-white border border-gray-300 rounded-md flex items-center justify-center hover:bg-gray-100 transition"
                                on:click={() => addToOrder(product)}
                            >
                                🛒
                            </button>

                            <!-- Tooltip Above -->
                            <span class="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-black text-white text-sm px-3 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                                Add to Cart
                            </span>
                        </div>
                    </div>
                </div>
            {/each}
        </div>  
    </div>

{:else if productView}

    <!-- consider making this a component, also justify-center centers it veritcaly -->
    <div class="flex flex-col items-center justify-center about-me w-full h-full overflow-y-auto">

        <!-- Card with Primary Color -->
        <div class="max-w-2xl mx-auto text-center p-6 bg-primary-500 text-primary-50 shadow-lg rounded-lg">
            <h1 class="text-3xl font-bold">{selectedProduct.name}</h1>
            
            <!-- The image is not working right now in the backend, will fix this later -->
            <!-- Product Image -->
            <!-- <img 
                class="w-full max-h-96 object-contain rounded-lg mx-auto mt-4 bg-primary-300" 
                src={product.image} 
                alt={product.name} 
            /> -->

            <!-- Price and Description -->
            <p class="text-lg font-semibold mt-4">${selectedProduct.price.toFixed(2)}</p>
            <h3 class="text-xl font-semibold mt-4">Description:</h3>
            <p class="mt-2">{selectedProduct.description}</p>

            <!-- Components List -->
            <h3 class="text-xl font-semibold mt-4">Components:</h3>
            <ul class="list-disc list-inside">
                {#each selectedProduct.components as component}
                    <li>{component}</li>
                {/each}
            </ul>

            <!-- Buttons (Stacked) -->
            <div class="flex flex-col gap-4 mt-6">
                <!-- Add to Cart Button -->
                <button 
                class="px-6 py-3 bg-white text-gray-800 border border-gray-400 rounded-lg hover:bg-gray-100 transition flex justify-center items-center text-center gap-2 w-full"
                    on:click={() => selectedProduct && addToOrder(selectedProduct)}
                >
                    🛒 Add to Cart
                </button>

                <!-- Back to Catalog Button -->
                <button 
                    class="px-4 py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 transition"
                    on:click={() => showCatalogView()}
                >
                    Back to Catalog
                </button>
            </div>

        </div>
    </div>  
{/if}