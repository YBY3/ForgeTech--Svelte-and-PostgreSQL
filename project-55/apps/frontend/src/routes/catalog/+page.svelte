<!-- <script>
    //import { orderStore } from "../stores/orderStore"; // Store to manage orders

    // Product name, product price, product description, product ingredients/components (ever product must have at least three components that make it up), product image, product id. 
  
    // Temporary mock product data (replace later with fetched data)
    let products = [
      {
        id: 1,
        name: "Sample GPU",
        price: 9.99,
        description: "Graphics Processing Unit",
        components: ["Color", "Make", "Year"],
        image: "/catalog-images/gpu.jpg"
      },
      {
        id: 2,
        name: "Sample CPU",
        price: 12.49,
        description: "Central Processing Unit",
        components: ["Color", "Make", "Year"],
        image: "/catalog-images/cpu.jpg"
      },
      {
        id: 3,
        name: "Sample Keyboard",
        price: 8.99,
        description: "Wireless Bluetooth Keyboard",
        components: ["Color", "Make", "Year"],
        image: "/catalog-images/keyboard.jpg"
      },

      {
        id: 4,
        name: "Sample GPU",
        price: 9.99,
        description: "Graphics Processing Unit",
        components: ["Color", "Make", "Year"],
        image: "/catalog-images/gpu.jpg"
      },
      {
        id: 5,
        name: "Sample CPU",
        price: 12.49,
        description: "Central Processing Unit",
        components: ["Color", "Make", "Year"],
        image: "/catalog-images/cpu.jpg"
      },
      {
        id: 6,
        name: "Sample Keyboard",
        price: 8.99,
        description: "Wireless Bluetooth Keyboard",
        components: ["Color", "Make", "Year"],
        image: "/catalog-images/keyboard.jpg"
      }
    ];
  
    // function addToOrder(product) {
    //   orderStore.addItem(product);
    // }

</script>
  
<div class ="flex flex-col w-full h-full overflow-y-auto">
  <br>
  <h1 class="text-center text-4xl font-medium">Our Products</h1>
  <br>
  <div class="catalog grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-4">
    {#each products as product}
      <div class="relative card variant-filled-primary card-hover rounded-lg shadow-md p-4">
        
        < Make Image Clickable -->
        <!-- <a href={`/catalog/${product.id}`}>
          <img 
            class="w-full h-48 object-cover rounded-md cursor-pointer transition-transform hover:scale-105" 
            src={product.image} 
            alt={product.name}
          />
        </a>
  
        <h2 class="text-lg font-semibold text-gray-800">{product.name}</h2>
        <p class="text-gray-600 text-sm">{product.description}</p>
        <p class="text-lg font-semibold text-gray-900">${product.price.toFixed(2)}</p>
  
        Add to Cart Icon -->
        <!-- <input 
          type="image" 
          class="absolute top-2 right-2 w-10 h-10 cursor-pointer transition-transform hover:scale-110" 
          src="/catalog-images/cart.jpg" 
          alt="Add To Cart" 
          title="Add To Cart"
        />
      </div>
    {/each}
  </div>
   
</div> -->

<script lang="ts">
  import { productStore, selectedProduct } from "$lib/StoreOrders/orders"; 
  import type { Product } from "$lib/StoreOrders/orders"; // ✅ Import Product type
  import { writable } from "svelte/store";

  // Use $productStore to access store reactively
  let products = $productStore;

  function selectProduct(product: Product) {  // ✅ Explicitly type 'product'
    selectedProduct.set(product);
  }

  // import { productStore } from "$lib/StoreOrders/orders"; 
  import { addToOrder } from "$lib/StoreOrders/orders"; 
</script>

<div class="flex flex-col w-full min-h-screen overflow-auto">
  <br>
  <h1 class="text-center text-4xl font-medium">Our Products</h1>
  <br>

  <!-- Catalog Grid -->
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6 overflow-y-auto">
    {#each $productStore as product}
      <div class="relative card variant-filled-primary card-hover rounded-lg shadow-md p-4">
        
        <!-- Make Image Clickable -->
        <a href="/catalog/expanded-view" on:click={() => selectProduct(product)}>
          <img 
            class="w-full h-48 object-cover rounded-md cursor-pointer transition-transform hover:scale-105" 
            src={product.image} 
            alt={product.name}
          />
        </a>        

        <h2 class="text-lg font-semibold text-gray-800">{product.name}</h2>
        <p class="text-gray-600 text-sm">{product.description}</p>
        <p class="text-lg font-semibold text-gray-900">${product.price.toFixed(2)}</p>

        <!-- Add to Cart Icon -->
      <button 
      class="absolute top-2 right-2 bg-blue-500 text-white p-2 rounded-full hover:bg-blue-600 transition"
      on:click={() => addToOrder(product)}
    >
      🛒
    </button>
      </div>
    {/each}
  </div>  
</div>


