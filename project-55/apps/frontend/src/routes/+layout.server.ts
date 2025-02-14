import { fetchFromFlask } from '$lib/api';
import type { ProductType } from "$lib/types/ProductTypes"

//Loads Data from Specified Link (products)
export const load = async () => {
    try {
        //Our Types Should Match the Backend Tables
        const products: ProductType[] = await fetchFromFlask('products');
        return { products: products };
    } catch (error) {
        console.error('Error:', error);
        return { data: null, error: 'Error Fetching Product Data' };
    }
};