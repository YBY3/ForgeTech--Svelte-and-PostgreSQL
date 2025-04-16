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

  let showAMD = false;
  let showNVIDIA = false;
  let showCorsair = false;
  let showNZXT = false;
  let showMSI = false;
  let showGIGABYTE = false;
  let showCooler_Master = false;
  let showSamsung = false;
  let showSanDisk = false;
  let showKingston = false;
  let showDELL = false;
  let showSeagate = false;

  let showINTEL = false;
  let showIBM = false;

  const ALLProducts = productsStore;
  
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

    if (showAMD) selectedBrands.push('AMD');
    if (showNVIDIA) selectedBrands.push('NVIDIA');
    if (showCorsair) selectedBrands.push('Corsair');
    if (showNZXT) selectedBrands.push('NZXT');
    if (showMSI) selectedBrands.push('MSI');
    if (showGIGABYTE) selectedBrands.push('GIGABYTE');
    if (showCooler_Master) selectedBrands.push('Cooler Master');
    if (showSamsung) selectedBrands.push('Samsung');
      if (showSanDisk) selectedBrands.push('SanDisk');
      if (showKingston) selectedBrands.push('Kingston');
      if (showDELL) selectedBrands.push('DELL');
      if (showSeagate) selectedBrands.push('Seagate');
      if (showINTEL) selectedBrands.push('INTEL');
      if (showIBM) selectedBrands.push('IBM');

// If no brand is selected, show all
if (selectedBrands.length === 0) {
  filterProducts = $ALLProducts;
  return;
}

filterProducts = $ALLProducts.filter(product =>
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
          <input class="checkbox" type="checkbox" bind:checked={showAMD} on:change={handleChange}/>
          <p>AMD</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showNVIDIA} on:change={handleChange}/>
          <p>NVIDIA</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showCorsair} on:change={handleChange}/>
          <p>CORSAIR</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showNZXT} on:change={handleChange}/>
          <p>NZXT</p>
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
          <input class="checkbox" type="checkbox" bind:checked={showCooler_Master} on:change={handleChange}/>
          <p>COOLER MASTER</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showSamsung} on:change={handleChange}/>
          <p>SAMSUNG</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showSanDisk} on:change={handleChange}/>
          <p>SANDISK</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showSeagate} on:change={handleChange}/>
          <p>SEAGATE</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showDELL} on:change={handleChange}/>
          <p>DELL</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showKingston} on:change={handleChange}/>
          <p>KINGSTON</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showINTEL} on:change={handleChange}/>
          <p>INTEL</p>
        </label>
        <label class="flex items-center space-x-2">
          <input class="checkbox" type="checkbox" bind:checked={showIBM} on:change={handleChange}/>
          <p>IBM</p>
        </label>
      </form>
</div>

  <div class="flex flex-col items-center w-full h-full bg-white dark:bg-black overflow-y-auto">
    
    <br>
    
    <h1 class="text-center text-4xl font-medium">Build It Your Way</h1>
    <h2 class="text-center text-2xl font-medium">Browse our full catalog of premium PC components — everything you need, all in one place.</h2>
    
    
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