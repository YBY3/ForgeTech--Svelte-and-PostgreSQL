import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL } from '$lib/api';
import type { ProductType } from '$lib/types/ProductTypes.js';


export const load = async ({ locals, fetch }) => {
    //Checks if User is Logged in
    if (!locals.user) {throw redirect(302, '/auth/login');}
    //Checks if User is a "employee"
    else if (locals.user.user_type != "employee") {throw redirect(302, '/catalog')}

    try {
        //Fetch All Products
        let response = await fetch(`${getFlaskURL()}/api/products/get_all_products`);
        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        const products: ProductType[] = await response.json();

        //Fetch Next Available Product ID
        response = await fetch(`${getFlaskURL()}/api/products/get_next_product_id`);
        if (!response.ok) {
            throw new Error('Failed to fetch next available Product ID');
        }
        const nextID = await response.json();

        return { products: products, nextID: nextID };
    } 
    catch (error) {
        console.error('Error fetching products:', error);
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
                images: formData.get('images'),
                product_type: formData.get('product_type'),
                product_stock: formData.get('product_stock')
            };

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

            return { success: true };
        } 
        
        catch (error) {
            console.error('Error in edit_product action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    },

    add_product: async ({ request }) => {
        try {
            const formData = await request.formData();
            const jsonData = {
                name: formData.get('name'),
                price: formData.get('price'),
                description: formData.get('description'),
                brand: formData.get('brand'),
                options: formData.get('options'),
                images: formData.get('images'),
                product_type: formData.get('product_type'),
                product_stock: formData.get('product_stock')
            };

            const flaskResponse = await fetch(`${getFlaskURL()}/api/products/add_product`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Adding Product Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                }
                return fail(flaskResponse.status, responseData);
            }

            return { success: true };
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