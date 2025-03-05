import { redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { ProductType } from '$lib/types/ProductTypes.js';


export const load = async ({ locals, fetch }) => {
    try {
        const response = await fetch(`${getFlaskURL()}/api/products/get_all_products`);

        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        const products: ProductType[] = await response.json();

        if (locals.user) {
            return { user: locals.user, products: products };
        } else {
            return { products: products };
        }
    } 
    
    catch (error) {
        console.error('Error fetching products:', error);
        return { products: [] as ProductType[] };
    }
};