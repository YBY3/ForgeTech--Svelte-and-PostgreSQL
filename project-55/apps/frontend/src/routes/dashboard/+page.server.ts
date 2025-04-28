import { fail, redirect } from '@sveltejs/kit';
import { getFlaskURL, getImageURL } from '$lib/api';
import type { OrderType } from '$lib/types/OrderTypes';
import type { UserType } from '$lib/types/UserTypes';
import type { ErrorResponseType } from '$lib/types/ResponseTypes';

type returnData = {
    user: {success: boolean, response: UserType} | null;
    userOrders: {success: boolean, response: OrderType[]} | ErrorResponseType | null;
    employeeClaimedOrders: {success: boolean, response: OrderType[]} | ErrorResponseType | null;
    users: {success: boolean, response: UserType[]} | ErrorResponseType | null;
    allOrders: {success: boolean, response: OrderType[]} | ErrorResponseType | null;
}

let returnData: returnData = {
    user: null,
    userOrders: null,
    employeeClaimedOrders: null,
    users: null,
    allOrders: null,
}

export const load = async ({ locals, fetch }) => {

    //Checks if User is Logged In
    if (!locals.user) {throw redirect(302, '/auth/login');}
    else {
        returnData.user = {success: true, response: locals.user};
    }

    //Load User Order Info
    if (locals.user.user_type == "customer" || locals.user.user_type == "admin") {

        try {
            let jsonData = {
                user_id: locals.user.id
            };

            //Fetch Orders via User ID
            let flaskResponse = await fetch(`${getFlaskURL()}/api/orders/get_all_orders`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Loading Orders Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                    returnData.userOrders = {success: false, response: {status: flaskResponse.status, error: responseData.error, message: responseData.message}}
                }
                else {
                    returnData.userOrders = {success: false, response: {status: flaskResponse.status, error: responseData.error, message: null}}
                }
            }
            else {
                returnData.userOrders = {success: true, response: responseData.orders};
            }
        } 
        catch (error) {
            console.error('Error Loading User Orders:', error);
        }
    }

    //Load Employee Info
    if (locals.user.user_type == "employee" || locals.user.user_type == "admin") {

        try {
            // let jsonData = {
            //     user_id: locals.user.id
            // };

            //Fetch Employee Claimed Orders via User ID
            let flaskResponse = await fetch(`${getFlaskURL()}/api/ordersControl/employeeDashboard/${locals.user.id}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Loading Employee Claimed Orders Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                    returnData.employeeClaimedOrders = {success: false, response: {status: flaskResponse.status, error: responseData.error, message: responseData.message}}
                }
                else {
                    returnData.employeeClaimedOrders = {success: false, response: {status: flaskResponse.status, error: responseData.error, message: null}}
                }
            }
            else {
                returnData.employeeClaimedOrders = {success: true, response: responseData.orders};
            }
        } 
        catch (error) {
            console.error('Error Loading Employee Claimed Orders:', error);
        }
    }

    //Load Admin Info
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
                    returnData.users = {success: false, response: {status: flaskResponse.status, error: responseData.error, message: responseData.message}}
                }
                else {
                    returnData.users = {success: false, response: {status: flaskResponse.status, error: responseData.error, message: null}}
                }
            }
            else {
                returnData.users = {success: true, response: responseData};
            }
        } 
        catch (error) {
            console.error('Error Loading Admin User Info:', error);
        }

        //Load All Order Data
        try {
            //Fetch All Orders
            let flaskResponse = await fetch(`${getFlaskURL()}/api/orders/getOrders`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Loading Order Data Failed:', responseData.error );
                if (responseData.message) {
                    console.error('Error:', responseData.message );
                    returnData.allOrders = {success: false, response: {status: flaskResponse.status, error: responseData.error, message: responseData.message}}
                }
                else {
                    returnData.allOrders = {success: false, response: {status: flaskResponse.status, error: responseData.error, message: null}}
                }
            }
            else {
                returnData.allOrders = {success: true, response: responseData.orders};
            }
        } 
        catch (error) {
            console.error('Error Loading Admin Order Info:', error);
        }
    }

    //Return Data
    if (returnData.userOrders != null || returnData.employeeClaimedOrders != null || returnData.users != null || returnData.allOrders != null) {
        console.error(returnData)
        return returnData;
    }
    else {
        // If this happens, something is really fucked up
        throw redirect(302, '/')
    }
}


export const actions = {
    unclaimOrder: async ({ request, fetch }) => {
        try {
            const formData = await request.formData();
            const jsonData = {
                order_id: formData.get('order_id')
            };

            const flaskResponse = await fetch(`${getFlaskURL()}/api/ordersControl/unclaim`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jsonData)
            });

            const responseData = await flaskResponse.json();

            if (!flaskResponse.ok) {
                console.error('Unclaiming Order Failed:', responseData.error );
                return fail(flaskResponse.status, responseData);
            }

            return { success: true, message: responseData.message };
        } 

        catch (error) {
            console.error('Error in unclaimOrder action:', error);
            return fail(500, { error: 'Internal Server Error' });
        }
    }
};