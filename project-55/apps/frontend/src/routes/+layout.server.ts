import { getFlaskURL, getImageURL } from "$lib/api";
import type { ProductType, RawProductType } from "$lib/types/ProductTypes";
import { fail } from "@sveltejs/kit"; // Use this instead of Node.js `assert`

export const load = async ({ locals, fetch }) => {
    const user = locals.user ?? null;

    try {
        // Fetch All Products
        const flaskResponse = await fetch(`${getFlaskURL()}/api/products/get_all_products`);
        const responseData = await flaskResponse.json();

        if (!flaskResponse.ok) {
            console.error('Failed to fetch products:', responseData.error);
            return fail(flaskResponse.status, responseData);
        }

        let productData: ProductType[] = [];

        if (responseData.data.length > 0) {
            productData = responseData.data.map((product: RawProductType) => ({
                ...product,
                image_urls: product.image_ids.map(id => `${getImageURL()}/api/images/${id}`)
            }));
        }

        return {
            user,
            products: productData
        };
    } catch (error) {
        console.error('Error Fetching Products:', error);
        return {
            user,
            products: [] as ProductType[]
        };
    }
};
