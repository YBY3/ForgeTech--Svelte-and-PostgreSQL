<script lang="ts">
    import { productsStore } from "$lib/stores/ProductsStore"; 
    import type { ProductType } from "$lib/types/ProductTypes";
    import ProductCard from "$lib/components/product/ProductCard.svelte";
  
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
          <ProductCard 
            product={product} 
            onProductSelect={(product) => {
              selectedProduct = product;
              showProductView();
            }} 
          />
        {/each}
      </div>  
    </div>
  
  {:else if productView}
  
    <!-- Product Detail View using ProductCard.svelte -->
    <div class="flex flex-col items-center justify-center about-me w-full h-full overflow-y-auto">
      <div class="w-1/3 mx-auto text-center p-6">
        <ProductCard product={selectedProduct} detailedView={true} />
        
        <!-- Back to Catalog Button -->
        <button 
          class="mt-6 px-4 py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 transition"
          on:click={() => showCatalogView()}
        >
          Back to Catalog
        </button>
      </div>
    </div>  
  {/if}