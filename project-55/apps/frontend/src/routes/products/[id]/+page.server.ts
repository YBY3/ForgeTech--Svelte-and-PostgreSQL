import { fail, error } from '@sveltejs/kit';
import { getFlaskURL, getImageURL } from '$lib/api';
import type { RawProductType, ProductType } from '$lib/types/ProductTypes';

export const load = async ({ params, locals, fetch }) => {
    try {
        const flaskResponse = await fetch(`${getFlaskURL()}/api/products/get_all_products`);
        const responseData = await flaskResponse.json();

        if (!flaskResponse.ok) {
            console.error('Failed to fetch products:', responseData.error);
            return fail(flaskResponse.status, responseData);
        }

        const productId = parseInt(params.id);
        const rawProduct = responseData.data.find((p: RawProductType) => p.id === productId);

        if (!rawProduct) {
            throw error(404, 'Product not found');
        }

        const product: ProductType = {
            ...rawProduct,
            image_urls: rawProduct.image_ids.map(id => `${getImageURL()}/api/images/${id}`)
        };

        let productData: ProductType[] = [];

        if (responseData.data.length > 0) {
            //Convert Image IDs to Image URLs
            productData = responseData.data.map((product: RawProductType) => ({
                ...product,
                image_urls: product.image_ids.map(id => `${getImageURL()}/api/images/${id}`)
            }));
        }

        let isLoggedIn = false;
        if (locals.user) {
            isLoggedIn = true;
        }

        return { product, isLoggedIn, productData };
    } catch (err) {
        console.error('Error loading product detail:', err);
        throw error(500, 'Failed to load product detail');
    }
};