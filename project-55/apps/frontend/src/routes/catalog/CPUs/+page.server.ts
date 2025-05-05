import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL, getImageURL } from '$lib/api';
import type { RawProductType, ProductType } from '$lib/types/ProductTypes.js';

export const load = async ({ locals, fetch }) => {
    if (locals.user) {
        if (locals.user.user_type == "employee") {
            throw redirect(302, '/');
        }
    }

    try {
        // Fetch All Products
        const flaskResponse = await fetch(`${getFlaskURL()}/api/products/get_all_products`);
        const responseData = await flaskResponse.json();

        if (!flaskResponse.ok) {
            console.error('Editing Product Failed:', responseData.error);
            if (responseData.message) {
                console.error('Error:', responseData.message);
            }
            return fail(flaskResponse.status, responseData);
        }

        let productData: ProductType[] = [];

        if (responseData.data.length > 0) {
            // Convert Image IDs to Image URLs and filter GPUs
            productData = responseData.data
                .filter((product: RawProductType) => product.product_type === "CPU")
                .map((product: RawProductType) => ({
                    ...product,
                    image_urls: product.image_ids.map(id => `${getImageURL()}/api/images/${id}`)
                }));
        }

        return { products: productData };
    } catch (error) {
        console.error('Error Fetching Products:', error);
        return { products: [] as ProductType[] };
    }
};
