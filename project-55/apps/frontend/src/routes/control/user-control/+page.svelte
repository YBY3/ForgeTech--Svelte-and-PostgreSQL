<script lang="ts">
    import { onMount } from 'svelte';
    import type { UserType } from "$lib/types/UserTypes"
    import { userstore, deleteUserFromStore } from "$lib/stores/UsersStore";

    export let data;
    let userData: UserType[] = [];
    let filterUsers: UserType[] = [];

    let showCustomers = true;
    let showEmployees = true;
    let showAdmins = true;
    

    function filterUsersfunc() {
    filterUsers = userData
        .filter(user => user.id !== data.localUser?.id) 
        .filter(user => {
            const isCustomer = showCustomers && user.user_type === 'customer';
            const isEmployee = showEmployees && user.user_type === 'employee';
            const isAdmin = showAdmins && user.user_type === 'admin';
            
            return isCustomer || isEmployee || isAdmin;
        });
    }

    
    onMount(() => {

        if (data.users) {
        userData = [...data.users].reverse(); 
        filterUsers = userData;
        filterUsers = userData.filter(user => user.id !== data.localUser?.id);
        }
    })

    function handleChange() {
        filterUsersfunc();
    }

    async function handleDelete(userId: string | number) {
    const formData = new FormData();
    formData.append('id', userId.toString()); 

    const response = await fetch('?/deleteUser', {  
        method: 'POST',  
        body: formData,   
    });

    if (!response.ok) {
        console.error("Failed to delete user");
    } else {
        console.log("User deleted successfully");
        window.location.reload();
    }
}

</script>


<div class="w-full flex justify-center pt-4 pr-4 pl-4">
    <div class="w-full h-16 flex justify-between items-center pl-4 pr-4 card variant-surface rounded-lg">
        <a 
            href="/dashboard"
            class="w-20 h-10 btn variant-ghost hover:text-primary-500 font-bold uppercase text-xl rounded-lg shadow-lg p-2" 
        >
            <i class="fa-solid fa-arrow-left"></i>
        </a>
        <h1 class="h-12 text-2xl md:text-3xl rounded-lg p-2 font-bold">User Control</h1>
        <div class="w-20"></div> <!-- Spacer -->
    </div>
</div>


<div class="h-full max-w-7xl mx-auto p-6 flex flex-col md:flex-row justify-between gap-x-10 overflow-x-hidden">
    
    <!-- User List (Left Side) -->
    <div class="w-full md:w-4/5 overflow-y-auto overflow-x-hidden">
        <div class="flex justify-between">
            <div>
            <p class="text-2xl font-bold">All Users</p>
            </div>

            <div>
                <a href="user-control/create-new-user"><button class="border-2 border-primary-500 rounded-lg p-2 hover:bg-primary-500 hover:text-white transition-colors duration-300"><i class="fa-solid fa-user-plus"></i> Create User</button></a>
            </div>

        </div>
        <br>
        <ul class="space-y-4">
            {#each filterUsers as user} 
                <li class="flex items-center justify-between p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover">
                    <span class="text-sm md:text-lg font-medium">{user.id}</span>
                    <span class="text-sm md:text-lg font-medium hidden sm:block">{user.username}</span>
                    <span class="text-sm md:text-lg">{user.email}</span>
                    <span class="text-sm md:text-lg">{user.user_type}</span>

                    <button 
                        class="text-red-500 hover:text-red-700 transition"
                        on:click={() => handleDelete(user.id)}>
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </li>
            {/each} 
        </ul>
    </div>
    
    <!-- Filter (Right Side) -->
    <div class="w-64 p-6 rounded-lg space-y-4">
        <p class="text-xl font-bold">Filters</p>
        <form class="space-y-2">
            <label class="flex items-center space-x-2">
              <input class="checkbox" type="checkbox" bind:checked={showCustomers} on:change={handleChange}/>
              <p>Customers</p>
            </label>
            <label class="flex items-center space-x-2">
              <input class="checkbox" type="checkbox" bind:checked={showEmployees} on:change={handleChange}/>
              <p>Employees</p>
            </label>
            <label class="flex items-center space-x-2">
              <input class="checkbox" type="checkbox" bind:checked={showAdmins} on:change={handleChange}/>
              <p>Administrators</p>
            </label>
          </form>
    </div>

</div>
