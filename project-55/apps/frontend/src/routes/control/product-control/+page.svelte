<script lang="ts">
    import { onMount } from 'svelte';
    import { invalidateAll } from '$app/navigation';
    import type { ActionResult } from '@sveltejs/kit';
    import { deserialize } from '$app/forms';
    import { getToastStore } from '@skeletonlabs/skeleton';
    import ProductSmallPreview from "$lib/components/product/ProductSmallPreview.svelte";
    import ProductForm from "$lib/components/product/ProductForm.svelte";
	import type { ProductType } from "$lib/types/ProductTypes";
	import { productsStore } from '$lib/stores/ProductsStore.js';

    //Tailwind Classes
    let navButtonClass = " w-full h-full btn text-xl hover:text-primary-500 font-bold uppercase rounded-lg ";
    let navContainerClass = " w-full md:w-3/4 grid grid-cols-2 gap-1 items-center justify-center card variant-soft rounded-lg p-1 ";

    function getActiveNavButtonClass(view: boolean) {
        return view ? "text-primary-500" : "hover:text-primary-500";
    }

    //Product Data
    export let data;
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

    async function showEditProductFormView(product: ProductType) {
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

    async function editProduct(product: ProductType, files: File[]) {
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
            formData.append('product_type', product.product_type);
            formData.append('product_stock', JSON.stringify(product.product_stock));
            formData.append('image_ids', JSON.stringify(product.image_ids));
            files.forEach((file, index) => {
                formData.append(`files[${index}]`, file);
            });

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/edit_product', {
                method: 'POST',
                body: formData
            });

            const result: ActionResult = deserialize(await response.text());

            if (result.type === 'success') {
                // Update Product Locally
                if (result.data) {
                    product.image_ids = result.data.image_ids
                    product.image_urls = result.data.image_urls
                }
                products = products.filter(p => p.id !== product.id);
                products.push(product)

                toastStore.trigger({
                    message: "Product Edited Successfully",
                    background: 'variant-filled-success'
                });
				showProductView();
            } 
            else if (result.type === 'failure') {
                if (result.data) {
                    const errorMessage = result.data.error;
                    throw new Error(errorMessage);
                }
                throw new Error("Server Error, Try Again Later");
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

    async function addProduct(product: ProductType, files: File[]) {
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
            formData.append('product_type', product.product_type);
            formData.append('product_stock', JSON.stringify(product.product_stock));
            files.forEach((file, index) => {
                formData.append(`files[${index}]`, file);
            });

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/add_product', {
                method: 'POST',
                body: formData
            });

            const result: ActionResult = deserialize(await response.text());

            if (result.type === 'success') {
                // Update Product Locally
                if (result.data) {
                    product.id = result.data.product_id;
                    product.image_ids = result.data.image_ids;
                    product.image_urls = result.data.image_urls;
                }
                products.push(product)

                toastStore.trigger({
                    message: "Product Added Successfully",
                    background: 'variant-filled-success'
                });
				showProductView();
            } 
            else if (result.type === 'failure') {
                if (result.data) {
                    const errorMessage = result.data.error;
                    throw new Error(errorMessage);
                }
                throw new Error("Server Error, Try Again Later");
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
        <div class="{navContainerClass}">
            <button on:click={() => showProductView()} class="{navButtonClass} {getActiveNavButtonClass(productsView)}">View Products</button>
            <button on:click={() => showAddProductFormView()} class="{navButtonClass} {getActiveNavButtonClass(addProductFormView)}">Add Product</button>
        </div>

        {#if productsView}
        
            <div class="w-full h-auto flex flex-col gap-4 items-center">
                {#if products.length > 0}
                    {#each products as product}
                        <div class="w-full h-auto md:w-3/4">
                            <ProductSmallPreview product={product} showOverlay={true}
                                on:edit={(event) => showEditProductFormView(event.detail.product)}
                                on:delete={(event) => deleteProduct(event.detail.product)}
                            />
                        </div>
                    {/each}
                {:else}
                    <div class="w-full md:w-3/4 h-auto card variant-ghost-error text-center rounded-lg p-4">
                        <div class="text-2xl font-bold">No Products Found!</div>
                        <div class="text-xl">if refreshing fails, we are working on fix</div>
                    </div>
                    <div class="w-full md:w-3/4 h-auto card variant-ghost-success text-center rounded-lg p-4">
                        <div class="text-2xl font-bold">No Products Added?</div>
                        <div class="text-xl">if products have not been added yet, start by adding one</div>
                    </div>
                {/if}
            </div>

        {:else if addProductFormView}

            <ProductForm on:submit={(event) => addProduct(event.detail.product, event.detail.files)}/> 

        {:else if editProductFormView}

            <ProductForm product={selectedProduct} on:submit={(event) => editProduct(event.detail.product, event.detail.files)}/> 

        {/if}

    </div>
{/if}