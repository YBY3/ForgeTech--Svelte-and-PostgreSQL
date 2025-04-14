import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { RawProductType, ProductType } from '$lib/types/ProductTypes.js';


export const load = async ({ locals, fetch }) => {
    //Checks if User is Logged in
    if (!locals.user) {throw redirect(302, '/auth/login');}
    //Checks if User is a "employee" or "admin"
    else if (locals.user.user_type != "employee" && locals.user.user_type != "admin") {throw redirect(302, '/')}

    try {
        //Fetch All Products
        const flaskResponse = await fetch(`${getFlaskURL()}/api/products/get_all_products`);
        
        const responseData = await flaskResponse.json();

        if (!flaskResponse.ok) {
            console.error('Editing Product Failed:', responseData.error );
            if (responseData.message) {
                console.error('Error:', responseData.message );
            }
            return fail(flaskResponse.status, responseData);
        }

        let productData: ProductType[] = [];

        if (responseData.data.length > 0) {
            //Convert Image IDs to Image URLs
            productData = responseData.data.map((product: RawProductType) => ({
                ...product,
                image_urls: product.image_ids.map(id => `${getFlaskURL()}/api/images/${id}`)
            }));
        }

        return { products: productData };
    } 
    catch (error) {
        console.error('Error Fetching Products:', error);
        return { products: [] as ProductType[] };
    }
};


export const actions = {
    edit_product: async ({ request }) => {
        try {
            const formData = await request.formData();

            const jsonData = {
                id: formData.get('id'),
                name: formData.get('name'),
                price: formData.get('price'),
                description: formData.get('description'),
                brand: formData.get('brand'),
                options: formData.get('options'),
                product_type: formData.get('product_type'),
                product_stock: formData.get('product_stock'),
                image_ids: formData.get('image_ids'),
                files: [] as { data: string; name: string; type: string }[]
            };

            // Add Images to jsonData
            for (const [key, value] of formData.entries()) {
                if (key.startsWith('files[')) {
                    const file = value as File;
                    const arrayBuffer = await file.arrayBuffer();
                    const base64Data = Buffer.from(arrayBuffer).toString('base64');
                    jsonData.files.push({
                        data: base64Data,
                        name: file.name,
                        type: file.type
                    });
                }
            }

            const flaskResponse = await fetch(`${getFlaskURL()}/api/products/edit_product`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Editing Product Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                }
                return fail(flaskResponse.status, responseData);
            }

            // Get Updated Image URLs
            let image_urls: string[] = [];
            if (responseData.image_ids && responseData.image_ids.length > 0) {
                image_urls = responseData.image_ids.map((id: number) => `${getFlaskURL()}/api/images/${id}`);
            }

            return { success: true, image_ids: responseData.image_ids, image_urls: image_urls };
        } 
        
        catch (error) {
            console.error('Error in edit_product action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    },

    add_product: async ({ request }) => {
        try {
            const formData = await request.formData();

            let jsonData = {
                name: formData.get('name'),
                price: formData.get('price'),
                description: formData.get('description'),
                brand: formData.get('brand'),
                options: formData.get('options'),
                product_type: formData.get('product_type'),
                product_stock: formData.get('product_stock'),
                files: [] as { data: string; name: string; type: string }[]
            };

            // Add Images to jsonData
            for (const [key, value] of formData.entries()) {
                if (key.startsWith('files[')) {
                    const file = value as File;
                    const arrayBuffer = await file.arrayBuffer();
                    const base64Data = Buffer.from(arrayBuffer).toString('base64');
                    jsonData.files.push({
                        data: base64Data,
                        name: file.name,
                        type: file.type
                    });
                }
            }

            let flaskResponse = await fetch(`${getFlaskURL()}/api/products/add_product`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            let responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Adding Product Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                }
                return fail(flaskResponse.status, responseData);
            }

            // Get Updated Product ID
            const product_id = responseData.product_id

            // Get Updated Image URLs
            let image_urls: string[] = [];
            if (responseData.image_ids && responseData.image_ids.length > 0) {
                image_urls = responseData.image_ids.map((id: number) => `${getFlaskURL()}/api/images/${id}`);
            }

            return { success: true, product_id: product_id, image_ids: responseData.image_ids, image_urls: image_urls };
        } 
        
        catch (error) {
            console.error('Error in add_product action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    },

    delete_product: async ({ request }) => {
        try {
            const formData = await request.formData();
            const jsonData = {
                id: formData.get('id'),
            };

            const flaskResponse = await fetch(`${getFlaskURL()}/api/products/delete_product`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Removing Product Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                }
                return fail(flaskResponse.status, responseData);
            }

            return { success: true };
        } 
        
        catch (error) {
            console.error('Error in delete_product action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    }
};