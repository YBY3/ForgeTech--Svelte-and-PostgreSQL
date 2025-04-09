<script lang="ts">
    import { onMount } from 'svelte';
    import { getToastStore } from '@skeletonlabs/skeleton';
    import ProductSmallPreview from "$lib/components/product/ProductSmallPreview.svelte";
    import ProductForm from "$lib/components/product/ProductForm.svelte";
	import type { ProductType } from "$lib/types/ProductTypes";
    //import * as imageUtils from "$lib/utils/imageUtils";

    //Tailwind Classes
    let navButtonClass = "w-full h-full btn variant-ringed text-xl hover:text-primary-500 font-bold uppercase rounded-lg";

    function getActiveNavButtonClass(view: boolean) {
        return view ? "text-primary-500" : "hover:text-primary-500";
    }

    //Product Data
    export let data;
    console.log(data);
    let products: ProductType[];
    let selectedProduct: ProductType;

    //Page Elements
    let submitting = false;
    const toastStore = getToastStore();

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

    onMount(() => {
        if (data.products) {
            products = data.products;
        }
    });

    async function editProduct(product: ProductType, file: File) {
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'Product Control is Submitting Changes, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        }

        //Try Submitting
        try {
            submitting = true;
            const formData = new FormData();
            formData.append('id', JSON.stringify(product.id));
            formData.append('name', product.name);
            formData.append('price', JSON.stringify(product.price));
            formData.append('description', product.description);
            formData.append('brand', product.brand);
            formData.append('options', JSON.stringify(product.options));
            formData.append('images', JSON.stringify(product.images));
            formData.append('product_type', product.product_type);
            formData.append('product_stock', JSON.stringify(product.product_stock));

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/edit_product', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            const parsedResultData = JSON.parse(result.data);
            const success = parsedResultData[parsedResultData[0].success];

            if (success) {
                toastStore.trigger({
                    message: "Product Edited Successfully",
                    background: 'variant-filled-success'
                });
                products = products.filter(p => p.id !== product.id);
                products.push(product)
				showProductView();
            }
            else {
				const errorMessage = parsedResultData[parsedResultData[0].error];
                throw new Error(errorMessage);
            }
        
        } catch (error) {
            const errorMessage: string = `${error}`;
			toastStore.trigger({
                message: errorMessage,
                background: 'variant-filled-error'
            });
        } finally {
            submitting = false;
        }
    }

    async function addProduct(product: ProductType) {
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'Product Control is Submitting Changes, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        }

        //Try Submitting
        try {
            submitting = true;
            const formData = new FormData();
            formData.append('name', product.name);
            formData.append('price', JSON.stringify(product.price));
            formData.append('description', product.description);
            formData.append('brand', product.brand);
            formData.append('options', JSON.stringify(product.options));
            formData.append('images', JSON.stringify(product.images));
            formData.append('product_type', product.product_type);
            formData.append('product_stock', JSON.stringify(product.product_stock));

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/add_product', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            const parsedResultData = JSON.parse(result.data);
            const success = parsedResultData[parsedResultData[0].success];

            if (success) {
                toastStore.trigger({
                    message: "Product Added Successfully",
                    background: 'variant-filled-success'
                });
                products.push(product)
				showProductView();
            }
            else {
				const errorMessage = parsedResultData[parsedResultData[0].error];
                throw new Error(errorMessage);
            }
        
        } catch (error) {
            const errorMessage: string = `${error}`;
			toastStore.trigger({
                message: errorMessage,
                background: 'variant-filled-error'
            });
        } finally {
            submitting = false;
        }
    }

    async function deleteProduct(product: ProductType) {
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'Product Control is Submitting Changes, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        }

        //Try Submitting
        try {
            submitting = true;
            const formData = new FormData();
            formData.append('id', JSON.stringify(product.id));

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/delete_product', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            const parsedResultData = JSON.parse(result.data);
            const success = parsedResultData[parsedResultData[0].success];

            if (success) {
                toastStore.trigger({
                    message: "Product Removed Successfully",
                    background: 'variant-filled-success'
                });
                products = products.filter(p => p.id !== product.id);
            }
            else {
				const errorMessage = parsedResultData[parsedResultData[0].error];
                throw new Error(errorMessage);
            }
        
        } catch (error) {
            const errorMessage: string = `${error}`;
			toastStore.trigger({
                message: errorMessage,
                background: 'variant-filled-error'
            });
        } finally {
            submitting = false;
        }
    }
</script>


{#if products}
    <div class="w-full h-full flex flex-col items-center gap-4 p-4 overflow-y-auto">

        <!-- Product View Options -->
        <div class="w-full md:w-3/4 grid grid-cols-1 md:grid-cols-2 gap-4 items-center justify-center card variant-soft rounded-lg p-4">
            <button on:click={() => showProductView()} class="{navButtonClass} {getActiveNavButtonClass(productsView)}">View Products</button>
            <button on:click={() => showAddProductFormView()} class="{navButtonClass} {getActiveNavButtonClass(addProductFormView)}">Add Product</button>
        </div>

        {#if productsView}
        
            <div class="w-full h-auto flex flex-col gap-4 items-center">
                {#each products as product}
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

            <ProductForm product={selectedProduct} on:submit={(event) => editProduct(event.detail.product, event.detail.file)}/> 

        {/if}

    </div>
{/if}