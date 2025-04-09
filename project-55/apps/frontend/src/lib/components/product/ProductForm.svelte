<script lang="ts">
    import { FileButton } from '@skeletonlabs/skeleton';
    import type { ProductType } from "$lib/types/ProductTypes"
    import { createEventDispatcher } from "svelte";

    //Tailwind Classes
    let inputClass = " input w-full md:w-3/4 h-[50px] min-h-[30px] focus:outline-none p-2 rounded-lg shadow-lg ";

    //Product Data
    export let product: ProductType | null = null;
    let file: File;
    
    let id = -1; //ID will be assigned on backend
    let name: string;
    let price: number;
    let description: string;
    let brand: string;
    let options: string;
    let images: string[] = [];
    let product_type: string;
    let product_stock: number;

    if (product != null) {
        id = product.id;
        name = product.name;
        price = product.price;
        description = product.description;
        brand = product.brand;
        options = product.options?.join(", ") || "No components";
        images = product.images;
        product_type = product.product_type;
        product_stock = product.product_stock;
    }

    const dispatch = createEventDispatcher();
    let imageChanged: boolean = false;
    let imageCount = 0;

    function handleFile(event: Event) {
        //Save File
        const input = event.target as HTMLInputElement;
        if (input.files && input.files[0]) {
            file = input.files[0];
        }

        imageChanged = true;
        imageCount += 1;

        //Get Image Path
        const fileExtension = file.name.split('.').pop()?.toLowerCase();
        const image = `/static/images/products/product_${id}_image_${imageCount}.${fileExtension}`;
        images.push(image);
    }

    function handleSubmit() {     
        dispatch("submit", { 
            product: {
                id: id,
                name: name,
                price: price,
                description: description,
                brand: brand,
                options: options.split(','),
                images: images,
                product_type: product_type,
                product_stock: product_stock
            },
            file: file
        });
    }
</script>


<form 
    on:submit|preventDefault={handleSubmit}
    class="flex flex-col gap-[1.5vh] w-full rounded-lg justify-center items-center text-base-content"  
>   
    <!-- Image -->
    {#if images[0] && !imageChanged}
        <img 
            class="w-full md:w-3/4 rounded-lg" 
            src={images[0]} 
            alt={name}
        />
    {/if}
    <div class="{inputClass}">
        <input
            id="image-field" 
            class="" 
            type="file" 
            on:change={handleFile}
            required 
        />
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