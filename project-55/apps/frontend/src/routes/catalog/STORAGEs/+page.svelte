<script lang="ts">
  import { onMount } from 'svelte';
  import type { ProductType } from "$lib/types/ProductTypes";
  import ProductCard from "$lib/components/product/ProductCard.svelte";
  import { goto } from '$app/navigation';
import { productsStore } from '$lib/stores/ProductsStore.js';
import { derived } from 'svelte/store';

  //Product Data
  export let data;
  let productData: ProductType[];

  //Page Elements
  let selectedProduct: ProductType;
  let catalogView = true;
  let productView = false;
  let isLoggedIn = false;

  const STORAGEProducts = derived(productsStore, ($products) =>
  $products.filter(p => p.product_type === 'STORAGE')
  );
  
  onMount(() => {
    if (data.user) {
      isLoggedIn = true;
    }
    if (data.products) {
        productData = data.products;
        productsStore.set(productData);
      }
  });
  function showCatalogView() {
      productView = false;
      catalogView = true;
  }

  function showProductView() {
      catalogView = false;
      productView = true;
  }
</script>

{#if $STORAGEProducts}
{#if catalogView}
  <div class="flex flex-col items-center w-full h-full overflow-y-auto">
    
    <br>
    
    <h1 class="text-center text-4xl font-medium">Our Products</h1>
    
    
    <br>
    <!-- Catalog Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6">
      {#each $STORAGEProducts as product}
        <ProductCard 
        product={product} 
        onProductSelect={(product) => goto(`/products/${product.id}`)} 
        isLoggedIn={isLoggedIn}
        />
      {/each}
    </div>  
  </div>

{:else if productView}

  <!-- Product Detail View using ProductCard.svelte -->
   <br>
  <div class="flex flex-col items-center justify-center about-me w-full h-full overflow-y-auto">
    <div class="w-1/3 mx-auto text-center p-6">
      <!--<ProductCard product={selectedProduct} detailedView={true} isLoggedIn={isLoggedIn} />-->
      
      <!-- Back to Catalog Button -->
      <button 
        class="mt-6 px-4 py-2 bg-primary-700 text-white rounded-lg hover:bg-primary-800 transition"
        on:click={() => showCatalogView()}
      >
        Back to Catalog
      </button> 
    </div>
    <br>
    <br> 
  </div> 
{/if}
{/if}