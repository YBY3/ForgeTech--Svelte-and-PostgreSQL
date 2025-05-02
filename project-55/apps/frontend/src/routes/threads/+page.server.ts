import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL, getImageURL } from '$lib/api';
import { stringify } from 'querystring';
import type { ThreadType } from '$lib/types/ThreadTypes.js';


export const load = async ({ locals, fetch }) => {
    //Checks if User is Logged In
    if (!locals.user) {throw redirect(302, '/auth/login');}

    //Checks if User is a "employee" or "admin"
        // else if (locals.user.user_type == "employee" || locals.user.user_type == "admin") {

        // try {
        //     //Fetch All Products
        //     const flaskResponse = await fetch(`${getFlaskURL()}/api/products/get_all_products`);
            
        //     const responseData = await flaskResponse.json();

        //     if (!flaskResponse.ok) {
        //         console.error('Editing Product Failed:', responseData.error );
        //         if (responseData.message) {
        //             console.error('Error:', responseData.message );
        //         }
        //         return fail(flaskResponse.status, responseData);
        //     }

        //     let productData: ProductType[] = [];

        //     if (responseData.data.length > 0) {
        //         //Convert Image IDs to Image URLs
        //         productData = responseData.data.map((product: RawProductType) => ({
        //             ...product,
        //             image_urls: product.image_ids.map(id => `${getImageURL()}/api/images/${id}`)
        //         }));
        //     }

        // return { user: locals.user };
        // } 
        // catch (error) {
        //     console.error('Error Fetching Products:', error);
        //     return { products: [] as ProductType[] };
        // }

    else {
        //Load Threads Via User ID
        try {
        
            const flaskResponse = await fetch(`${getFlaskURL()}/api/threads/get_threads?user_id=${locals.user.id}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Loading Threads Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                }
                return fail(flaskResponse.status, responseData);
            }

            return { user: locals.user, threads: responseData.threads };
        } 
        catch (error) {
            console.error('Error Fetching Threads:', error);
            return { user: locals.user, threads: [] as ThreadType[] };
        }
    }

    // }
    // else {
    //     throw redirect(302, '/')
    // }
};


export const actions = {

    add_thread: async ({ request }) => {
        try {
            const formData = await request.formData();

            let jsonData = {
                name: formData.get('name'),
                user_id: formData.get('user_id'),
            };

            let flaskResponse = await fetch(`${getFlaskURL()}/api/threads/add_thread`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            let responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Adding Thread Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                }
                return fail(flaskResponse.status, responseData);
            }

            return { success: true, thread: responseData.thread };
        } 
        
        catch (error) {
            console.error('Error in add_thread action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    },

    get_thread_messages: async ({ request }) => {
        try {
            const formData = await request.formData();

            let jsonData = {
                thread_id: formData.get('thread_id'),
            };

            let flaskResponse = await fetch(`${getFlaskURL()}/api/threads/get_thread_messages`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            let responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Loading Thread Messages Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                }
                return fail(flaskResponse.status, responseData);
            }

            console.error(responseData)

            // return { success: true, thread: responseData.thread };
        } 
        
        catch (error) {
            console.error('Error in get_thread_messages action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    },

    send_message: async ({ request }) => {
        try {
            const formData = await request.formData();

            let jsonData = {
                thread_id: formData.get('thread_id'),
                user_id: formData.get('user_id'),
                responding_to_id: formData.get('responding_to_id'),
                message: formData.get('message'),
            };

            let flaskResponse = await fetch(`${getFlaskURL()}/api/threads/add_message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            let responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Adding Message to Thread Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                }
                return fail(flaskResponse.status, responseData);
            }

            console.error(responseData)

            // return { success: true, thread: responseData.thread };
        } 
        
        catch (error) {
            console.error('Error in send_message action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    }
};