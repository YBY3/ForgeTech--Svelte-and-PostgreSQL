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
    let showMSI = false;
    let showGIGABYTE = false;
    let showASUS = false;
  
    const gpuProducts = derived(productsStore, ($products) =>
    $products.filter(p => p.product_type === 'GPU')
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

      if (showAMD) selectedBrands.push('AMD');
      if (showNVIDIA) selectedBrands.push('NVIDIA');
      if (showMSI) selectedBrands.push('MSI');
      if (showGIGABYTE) selectedBrands.push('GIGABYTE');
      if (showASUS) selectedBrands.push('ASUS');

  // If no brand is selected, show all
  if (selectedBrands.length === 0) {
    filterProducts = $gpuProducts;
    return;
  }

  filterProducts = $gpuProducts.filter(product =>
    selectedBrands.includes(product.brand)
  );
  }
  


  function handleChange() {
        changer();
    }
  </script>
  
  {#if $gpuProducts}
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
      
      <h1 class="text-center text-4xl font-medium">Graphics Unleashed</h1>
      <h2 class="text-center text-2xl font-medium">Experience stunning visuals and ultra-fast performance with our top-tier GPUs.</h2>
      
      
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
  {/if}