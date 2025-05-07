import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL, getImageURL } from '$lib/api';
import type { UserType } from '$lib/types/UserTypes';
import type { ProductType, RawProductType } from '$lib/types/ProductTypes';
import type { OrderProductType, OrderType } from '$lib/types/OrderTypes';

let users: UserType[];
let orderData: OrderType[] = [];
let orderProductData: OrderProductType[] = [];

export const load = async ({ locals, fetch }) => {
    //Checks if User is Logged In
    if (!locals.user) {throw redirect(302, '/auth/login');}

        //Get users
        if (locals.user.user_type == "admin") {
    
            //Load All User Data
            try {
                //Fetch All Users
                let flaskResponse = await fetch(`${getFlaskURL()}/api/users/get_users`, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' }
                });
    
                const responseData = await flaskResponse.json();
    
                if (!flaskResponse.ok) {
                    console.error('Loading User Data Failed:', responseData.error );
                    if (responseData.message) {
                        console.error('Error:', responseData.message );
                    }
                    // return fail(flaskResponse.status, responseData);
                }
    
                users = responseData;
    
                // return { user: locals.user, userOrders: userOrders };
            } 
            catch (error) {
                console.error('Error Loading Admin User Info:', error);
            }

            try {
                // Fetch All orders
                const flaskResponse = await fetch(`${getFlaskURL()}/api/orders/actually_get_all_orders`);
                const responseData = await flaskResponse.json();
        
                if (!flaskResponse.ok) {
                    console.error('Failed to fetch orders:', responseData.error);
                    return fail(flaskResponse.status, responseData);
                }
        
                // console.log(orderData);
                orderData = responseData;
        
                
            } catch (error) {
                console.error('Error Fetching Orders:', error);
            }

            try {
                // Fetch All orders
                const flaskResponse = await fetch(`${getFlaskURL()}/api/orders/get_all_OrderProducts`);
                const responseData = await flaskResponse.json();
        
                if (!flaskResponse.ok) {
                    console.error('Failed to fetch order products:', responseData.error);
                    return fail(flaskResponse.status, responseData);
                }
        
                // console.log(orderData);
                orderProductData = responseData;
        
                
            } catch (error) {
                console.error('Error Fetching Order Products:', error);
            }

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
                    user: locals.user,
                    users: users,
                    products: productData,
                    orders: orderData,
                    orderProduct: orderProductData
                };
            } catch (error) {
                console.error('Error Fetching Products:', error);
                return {
                    user: locals.user,
                    users: users,
                    products: [] as ProductType[],
                    orders: orderData
                };
            }
    
        }

}