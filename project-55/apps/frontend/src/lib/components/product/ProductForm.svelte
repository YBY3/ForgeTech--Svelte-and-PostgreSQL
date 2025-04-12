<script lang="ts">
    import { FileButton } from '@skeletonlabs/skeleton';
    import type { ProductType } from "$lib/types/ProductTypes"
    import { createEventDispatcher } from "svelte";

    //Tailwind Classes
    let inputClass = " input w-full md:w-3/4 h-[50px] min-h-[30px] focus:outline-none p-2 rounded-lg shadow-lg ";

    //Product Data
    export let product: ProductType | null = null;
    let file: File;
    
    let id = -1; //this is temp, this should be the highest index in the table
    let name: string;
    let price: number;
    let description: string;
    let components: string;
    let image: string;

    if (product != null) {
        id = product.id;
        name = product.name;
        price = product.price;
        description = product.description;
        components = product.components?.join(", ") || "No components";
        image = product.image;
    }

    const dispatch = createEventDispatcher();
    let imageChanged: boolean = false;

    function handleFile(event: Event) {
        //Save File
        const input = event.target as HTMLInputElement;
        if (input.files && input.files[0]) {
            file = input.files[0];
        }

        imageChanged = true;

        //Get Image Path
        const fileExtension = file.name.split('.').pop()?.toLowerCase();
        const image = `/static/images/products/product_${id}.${fileExtension}`;
    }

    function handleSubmit() {     
        dispatch("submit", { 
            product: {
                id: id,
                name: name,
                price: price,
                description: description,
                components: components.split(','),
                image: image
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
    {#if image && !imageChanged}
        <img 
            class="w-full md:w-3/4 rounded-lg" 
            src={image} 
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

    <!-- Components -->
    <input
        id="components-field" 
        class="{inputClass}" 
        type="text" 
        placeholder="Product Components"
        bind:value={components} 
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