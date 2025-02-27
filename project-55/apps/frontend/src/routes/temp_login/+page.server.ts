// // import { fetchFromFlask } from '$lib/api';
// // import type { UserType } from "$lib/types/UserTypes"

// // // //CALL FROM SERVER
// // // export async function get() {
// // //     const user = await fetchFromFlask<UserType>('temp_login');
// // //     return {
// // //         status: 200,
// // //         body: user
// // //     };
// // // }


// // export async function post({ request }) {
// //     const { username, password } = await request.json();

// //     const response = await fetch('http://localhost:6150/temp_login',  { // Your Flask server URL
// //         method: 'POST',
// //         headers: { 'Content-Type': 'application/json' },
// //         body: JSON.stringify({ username, password })
// //     });

// //     const result = await response.json();

// //     if (response.ok) {
// //         return {
// //             status: 200,
// //             body: result // Send user data back to frontend
// //         };
// //     } else {
// //         return {
// //             status: 401,
// //             body: { message: result.message }
// //         };
// //     }
// // }


// // import { fetchFromFlask } from '$lib/api'; 
// // import type { UserType } from "$lib/types/UserTypes"

// // export async function post({ request }) {
// //     // Extract username and password from the frontend request
// //     const { username, password } = await request.json();

// //     // Send a POST request to Flask backend
// //     const response = await fetch('http://localhost:6150/temp_login', {  // Ensure your Flask server is on this port
// //         method: 'POST',
// //         headers: { 'Content-Type': 'application/json' },
// //         body: JSON.stringify({ username, password }) // Sending login data to Flask
// //     });

// //     // Parse the JSON response from the backend
// //     const result = await response.json();

// //     // If the response is successful, return user data to the frontend
// //     if (response.ok) {
// //         return {
// //             status: 200,
// //             body: result  // Send user data back to frontend on successful login
// //         };
// //     } else {
// //         // If login fails, return an error message
// //         return {
// //             status: 401,  // Unauthorized
// //             body: { message: result.message || 'Login failed' }
// //         };
// //     }
// // }

// import type { RequestEvent } from '@sveltejs/kit';  // Import RequestEvent type from SvelteKit
// import { fetchFromFlask } from '$lib/api'; 
// import type { UserType } from "$lib/types/UserTypes"

// // Post function to handle login
// export async function post({ request }: RequestEvent) {  // Type the 'request' parameter
//     // Extract username and password from the frontend request
//     const { username, password } = await request.json();

//     // Send a POST request to Flask backend
//     const response = await fetch('http://localhost:6150/temp_login', {  // Ensure your Flask server is on this port
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ username, password }) // Sending login data to Flask
//     });

//     // Parse the JSON response from the backend
//     const result = await response.json();

//     // If the response is successful, return user data to the frontend
//     if (response.ok) {
//         return {
//             status: 200,
//             body: result  // Send user data back to frontend on successful login
//         };
//     } else {
//         // If login fails, return an error message
//         return {
//             status: 401,  // Unauthorized
//             body: { message: result.message || 'Login failed' }
//         };
//     }
// }

// import type { RequestHandler } from "@sveltejs/kit";

// export const POST: RequestHandler = async ({ request }) => {
//   try {
//     const { username, email, password } = await request.json();

//     const response = await fetch("http://localhost:5000/signup", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ username, email, password }),
//     });

//     if (!response.ok) {
//       throw new Error("Signup failed");
//     }

//     return new Response(JSON.stringify({ message: "Signup successful!" }), { status: 200 });
//   } catch (error) {
//     return new Response(JSON.stringify({ message: error.message }), { status: 500 });
//   }
// };

import type { RequestHandler } from "@sveltejs/kit";

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { username, email, password } = await request.json();
    
    // Log values to ensure they're being received correctly
    console.log({ username, email, password });

    const response = await fetch("http://localhost:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    if (!response.ok) {
      // Log the response status if it's not OK
      console.error("Error response:", await response.text());
      throw new Error("Signup failed");
    }

    return new Response(JSON.stringify({ message: "Signup successful!" }), { status: 200 });
  } catch (error: any) {
    // Log the error to understand more about the failure
    console.error("Error during signup:", error);
    return new Response(JSON.stringify({ message: error.message }), { status: 500 });
  }
};
