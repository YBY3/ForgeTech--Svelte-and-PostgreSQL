import { writable } from "svelte/store";
import type { UserType } from "$lib/types/UserTypes"
import { getFlaskURL } from "$lib/api";

export const userstore = writable<UserType[]>([]);

export function addUserToStore(user: UserType){
    userstore.update(users => [...users, user])
}

export async function deleteUserFromStore(userId: string | number) {
    try {
        // Make the API request to delete the user from the database
        console.log("AHHHHH")
        const response = await fetch(`${getFlaskURL()}/users/delete_user`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify(userId) 
        });

        if (!response.ok) {
            throw new Error('Failed to delete user from the database');
        }

        // If successful, update the store to remove the user from the UI
        userstore.update(users => users.filter(user => user.id !== userId));
    } catch (error) {
        console.error("Error deleting user:", error);
    }
}