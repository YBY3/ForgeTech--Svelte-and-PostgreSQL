<script lang="ts">
    import { onDestroy } from 'svelte';
    import { FileDropzone } from '@skeletonlabs/skeleton';
    import { createEventDispatcher } from "svelte";
    import { getToastStore } from '@skeletonlabs/skeleton';
    import type { ProductType } from "$lib/types/ProductTypes"
    import type { ImageType } from "$lib/types/ImageTypes"

    //Tailwind Classes
    let inputClass = " input w-full md:w-3/4 h-[50px] min-h-[30px] focus:outline-none p-2 rounded-lg shadow-lg ";

    //Product Data
    export let product: ProductType | null = null;

    //Image Elements
    let imageFiles: File[] = []; 
    let imagePreviews: string[] = []; 

    //Form Elements
    const dispatch = createEventDispatcher();
    const toastStore = getToastStore();
    let id = -1; //ID will be assigned on backend
    let name: string;
    let price: number;
    let description: string;
    let brand: string;
    let options: string;
    let product_type: string;
    let product_stock: number;
    let image_ids: number[] = [];
    let image_urls: string[] = [];

    if (product != null) {
        id = product.id;
        name = product.name;
        price = product.price;
        description = product.description;
        brand = product.brand;
        options = product.options?.join(", ") || "No components";
        product_type = product.product_type;
        product_stock = product.product_stock;
        image_ids = product.image_ids;
        image_urls = product.image_urls;
    }

    function handleFile(event: Event) {
        const input = event.target as HTMLInputElement;
        const files = input.files ? Array.from(input.files) : [];

        if (files.length === 0) return;

        if ((image_ids.length + imageFiles.length) === 5) {
            toastStore.trigger({
                message: `Only 5 Images Allowed`,
                background: 'variant-filled-error',
            });
            return;
        }

        const ALLOWED_MIMETYPES = ['image/jpeg', 'image/png', 'image/gif'];
        const validFiles: File[] = [];
        const newPreviews: string[] = [];

        files.forEach((file) => {
            if (ALLOWED_MIMETYPES.includes(file.type)) {
                validFiles.push(file);
                newPreviews.push(URL.createObjectURL(file));
            } else {
                toastStore.trigger({
                    message: `File Type Not Allowed`,
                    background: 'variant-filled-error',
                });
            }
        });

        if (validFiles.length > 0) {
            imageFiles = [...imageFiles, ...validFiles];
            imagePreviews = [...imagePreviews, ...newPreviews];
        }
    }

    function removeImage(index: number) {
        // Revoke Preview URL
        URL.revokeObjectURL(imagePreviews[index]);
        // Remove from Arrays
        imageFiles = imageFiles.filter((_, i) => i !== index);
        imagePreviews = imagePreviews.filter((_, i) => i !== index);
    }

    function handleSubmit() {
        if (!name || !price || !description || !brand || !options || !product_type || !product_stock) {
            toastStore.trigger({
                message: 'Required Fields Missing',
                background: 'variant-filled-error',
            });
            return;
        }

        if (imageFiles.length === 0 && image_ids.length === 0) {
            toastStore.trigger({
                message: 'At Least One Image is Required',
                background: 'variant-filled-error',
            });
            return;
        }

        dispatch('submit', {
            product: {
                id,
                name,
                price,
                description,
                brand,
                options: options.split(',').map((opt) => opt.trim()),
                product_type,
                product_stock,
                image_ids: image_ids,
                image_urls: image_urls,
            },
            files: imageFiles
        });
    }

    onDestroy(() => {
        imagePreviews.forEach((preview) => URL.revokeObjectURL(preview));
    });
</script>


<form 
    on:submit|preventDefault={handleSubmit}
    class="flex flex-col gap-[1.5vh] w-full rounded-lg justify-center items-center text-base-content"  
>   
    <!-- Images -->
    <div class="flex gap-4 w-full md:w-3/4 overflow-x-auto">

        <div class="{imageFiles.length > 0 || image_ids.length > 0 ? 'flex-none w-[350px]' : 'flex-1 w-full'} h-[300px] card variant-soft rounded-lg">
            <FileDropzone name="files" rounded="rounded-lg" class="h-full flex flex-col justify-center items-center" multiple on:change={handleFile}>
                <svelte:fragment slot="lead">
                    <i class="fa-solid fa-plus text-8xl"></i>
                </svelte:fragment>
                <svelte:fragment slot="message">
                    <h2 class="text-2xl">Add Image</h2>
                </svelte:fragment>
                <svelte:fragment slot="meta">
                    <h3 class="text-xl">JPG / JPEG, PNG, and GIF Only</h3>
                </svelte:fragment>
            </FileDropzone>
        </div>

        <!-- Existing Images -->
        {#if image_urls.length > 0}
            {#each image_urls as image_url, i}
                <div class="flex-none relative h-[300px] rounded-lg">
                    {#if image_url}
                        <img
                            class="h-[300px] object-contain rounded-lg"
                            src={image_url}
                            alt={'Existing Image'}
                        />
                    {/if}
                    <button
                        type="button"
                        class="absolute top-2 right-2 btn btn-sm variant-filled-error"
                        on:click={() => {
                            image_ids = image_ids.filter((_, idx) => idx !== i);
                            image_urls = image_urls.filter((_, idx) => idx !== i);
                        }}
                    >
                        X
                    </button>
                </div>
            {/each}
        {/if}

        <!-- New Images -->
        {#if imagePreviews.length > 0}
            {#each imagePreviews as preview, index}
                <div class="flex-none relative h-[300px] rounded-lg">
                    <img 
                        class="h-[300px] object-contain rounded-lg" 
                        src={preview} 
                        alt={name || 'Uploaded Image'}
                    />
                    <button 
                        type="button"
                        class="absolute top-2 right-2 btn btn-sm variant-filled-error" 
                        on:click={() => removeImage(index)}
                    >
                        X
                    </button>
                </div>
            {/each}
        {/if}
    </div>

    <!-- Name -->
    <input
        id="name-field" 
        class="{inputClass}" 
        type="text" 
        placeholder="Product Name"
        bind:value={name} 
        required 
    />

    <!-- Price -->
    <input
        id="price-field" 
        class="{inputClass}" 
        type="number" 
        placeholder="Product Price ($)"
        step="0.01"
        min="0"
        bind:value={price} 
        required 
    />

    <!-- Description -->
    <textarea
        id="description-field" 
        class="{inputClass}" 
        placeholder="Product Description"
        bind:value={description} 
        required 
    />

    <!-- Brand -->
    <input
        id="brand-field" 
        class="{inputClass}" 
        type="text" 
        placeholder="Product Brand"
        bind:value={brand} 
        required 
    />

    <!-- Options -->
    <input
        id="options-field" 
        class="{inputClass}" 
        type="text" 
        placeholder="Product Options (example: color, size options, spec options, etc)"
        bind:value={options} 
        required 
    />

    <!-- Product Type -->
    <input
        id="product-type-field" 
        class="{inputClass}" 
        type="text" 
        placeholder="Product Type"
        bind:value={product_type} 
        required 
    />

    <!-- Product Stock -->
    <input
        id="price-field" 
        class="{inputClass}" 
        type="number" 
        placeholder="Product Stock"
        step="1"
        min="0"
        bind:value={product_stock} 
        required 
    />

    <!-- Submit Button -->
    <div class="pt-4">
        <button 
            type="submit"
            class="w-[150px] h-[50px] btn variant-ghost hover:text-primary-500 font-bold uppercase text-2xl rounded-lg shadow-lg" 
        >
            Save
        </button>
    </div>
</form>