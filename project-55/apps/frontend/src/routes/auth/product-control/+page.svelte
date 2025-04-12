<script lang="ts">
    import { productsStore, replaceProductInStore, addProductToStore, deleteProductFromStore } from "$lib/stores/ProductsStore"; 
    import ProductSmallPreview from "$lib/components/product/ProductSmallPreview.svelte";
    import ProductForm from "$lib/components/product/ProductForm.svelte";
	import type { ProductType } from "$lib/types/ProductTypes";
    //import * as imageUtils from "$lib/utils/imageUtils";

    //Tailwind Classes
    let navButtonClass = "w-full h-full btn variant-ringed text-xl hover:text-primary-500 font-bold uppercase rounded-lg";

    function getActiveNavButtonClass(view: boolean) {
        return view ? "text-primary-500" : "hover:text-primary-500";
    }

    //Page Views
    let productsView = true;
    let addProductFormView = false;
    let editProductFormView = false;

    function showProductView() {
        addProductFormView = false;
        editProductFormView = false;
        productsView = true;
    }

    function showAddProductFormView() {
        editProductFormView = false;
        productsView = false;
        addProductFormView = true;
    }

    function showEditProductFormView(product: ProductType) {
        selectedProduct = product;

        addProductFormView = false;
        productsView = false;
        editProductFormView = true;
    }

    //Product Controls
    let selectedProduct: ProductType;

    function replaceProduct(product: ProductType, file: File) {
        showProductView();
        replaceProductInStore(product);
    }

    function addProduct(product: ProductType) {
        showProductView();
        addProductToStore(product);
    }

    function deleteProduct(product: ProductType) {
        deleteProductFromStore(product.id);
    }
</script>


<div class="w-full h-full flex flex-col items-center gap-4 p-4 overflow-y-auto">

    <!-- Product View Options -->
    <div class="w-full md:w-3/4 grid grid-cols-1 md:grid-cols-2 gap-4 items-center justify-center card variant-soft rounded-lg p-4">
        <button on:click={() => showProductView()} class="{navButtonClass} {getActiveNavButtonClass(productsView)}">View Products</button>
        <button on:click={() => showAddProductFormView()} class="{navButtonClass} {getActiveNavButtonClass(addProductFormView)}">Add Product</button>
    </div>

    {#if productsView}
    
        <div class="w-full h-auto flex flex-col gap-4 items-center">
            {#each $productsStore as product}
                <div class="w-full h-auto md:w-3/4">
                    <ProductSmallPreview product={product} showOverlay={true}
                        on:edit={(event) => showEditProductFormView(event.detail.product)}
                        on:delete={(event) => deleteProduct(event.detail.product)}
                    />
                </div>
            {/each}
        </div>

    {:else if addProductFormView}

        <ProductForm on:submit={(event) => addProduct(event.detail.product)}/> 

    {:else if editProductFormView}

        <ProductForm product={selectedProduct} on:submit={(event) => replaceProduct(event.detail.product, event.detail.file)}/> 

    {/if}

</div>