import { getFlaskURL } from '$lib/api';
import type { ProductType } from '$lib/types/ProductTypes.js';


export const load = async ({ fetch }) => {
    try {
        const response = await fetch(`${getFlaskURL()}/products`);

        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        const products: ProductType[] = await response.json();
        return { products: products };
    } 
    
    catch (error) {
        console.error('Error fetching products:', error);
        return { products: [] as ProductType[] };
    }
};