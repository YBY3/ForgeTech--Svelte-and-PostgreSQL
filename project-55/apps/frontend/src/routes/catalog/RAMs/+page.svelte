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
  let filterProducts: ProductType[] = [];

  //Page Elements
  let catalogView = true;
  let isLoggedIn = false;


  let showCorsair = false;
  let showSamsung = false;
  let showMSI = false;
  let showGIGABYTE = false;
  let showASUS = false;

  const RAMProducts = derived(productsStore, ($products) =>
  $products.filter(p => p.product_type === 'RAM')
  );
  
  onMount(() => {
    if (data.user) {
      isLoggedIn = true;
    }
    if (data.products) {
      productData = data.products;
      productsStore.set(productData);
    }

    changer()
  });
  


  function changer() {
  const selectedBrands: string[] = [];

    if (showCorsair) selectedBrands.push('Corsair');
    if (showSamsung) selectedBrands.push('Samsung');
    if (showMSI) selectedBrands.push('MSI');
    if (showGIGABYTE) selectedBrands.push('GIGABYTE');
    if (showASUS) selectedBrands.push('ASUS');

// If no brand is selected, show all
if (selectedBrands.length === 0) {
  filterProducts = $RAMProducts;
  return;
}

filterProducts = $RAMProducts.filter(product =>
  selectedBrands.includes(product.brand)
);
}



function handleChange() {
      changer();
  }
</script>


{#if catalogView}

<div class="flex flex-row items-center w-full h-full bg-white dark:bg-black overflow-y-auto">
  <!-- Filter (Left Side) -->
  <div class="w-64 p-6 rounded-lg space-y-4 hidden sm:block">
    <p class="text-xl font-bold">Brand</p>
    <form class="space-y-2">
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showCorsair} on:change={handleChange}/>
          <p>CORSAIR</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showSamsung} on:change={handleChange}/>
          <p>SAMSUNG</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showMSI} on:change={handleChange}/>
          <p>MSI</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showGIGABYTE} on:change={handleChange}/>
          <p>GIGABYTE</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showASUS} on:change={handleChange}/>
          <p>ASUS</p>
        </label>
      </form>
</div>

  <div class="flex flex-col items-center w-full h-full bg-white dark:bg-black overflow-y-auto">
    
    <br>
    
    <h1 class="text-center text-4xl font-medium">Speed Meets Memory</h1>
    <h2 class="text-center text-2xl font-medium">Boost your system’s multitasking and responsiveness with high-performance RAM.</h2>
    
    
    <br>
    <!-- Catalog Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-6">
      {#each filterProducts as product}
        <ProductCard 
        product={product} 
        onProductSelect={(product) => goto(`/products/${product.id}`)} 
        isLoggedIn={isLoggedIn}
        />
      {/each}
    </div>  
  </div>
</div>

{/if}
