<script lang="ts">
    import { onMount } from 'svelte';
    import type { ActionResult } from '@sveltejs/kit';
    import { deserialize } from '$app/forms';
    import { getToastStore, Avatar, FileButton } from '@skeletonlabs/skeleton';
    import OrderInfoCard from '$lib/components/order/OrderInfoCard.svelte';
    import type { UserType } from '$lib/types/UserTypes.js';
    import type { OrderType } from '$lib/types/OrderTypes';

    export let data;
    let userData: UserType;
    let userOrders: OrderType[];
    let employeeClaimedOrders: OrderType[];
    let users: UserType[]
    let allOrders: OrderType[]

    //Page Elements
    let recentlyRegisteredUsers: UserType[];
    let recentlyActiveUsers: UserType[];
    let recentlyPlacedOrders: OrderType[]

    onMount(() => {
        if (data.user) {
            userData = data.user;
        }

        if (data.userOrders) {
            userOrders = data.userOrders;
        }

        if (data.employeeClaimedOrders) {
            employeeClaimedOrders = data.employeeClaimedOrders;
        }

        if (data.users) {
            users = data.users;

            //Sort By Recently Registered
            recentlyRegisteredUsers = users
				.sort((a: any, b: any) => new Date(a.registered_by).getTime() - new Date(b.registered_by).getTime())

            //Sort by Recently Active
            recentlyActiveUsers = users
				.sort((a: any, b: any) => new Date(b.active_by).getTime() - new Date(a.active_by).getTime())
        }

        if (data.allOrders) {
            allOrders = data.allOrders;

            //Sort by Recently Placed
            recentlyPlacedOrders = allOrders
			.sort((a: OrderType, b: OrderType) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        }
    });

</script>


{#if userData}
    <!-- Dashboard -->
    <div class="w-full h-full flex flex-col items-center ">

        <h1 class="text-5xl p-8">Dashboard</h1>

        <!-- Dashboard Grid -->
        <div class="w-full md:w-3/4 grid grid-cols-1 lg:grid-cols-2 gap-4 pt-4">

            <!-- User Information -->
            <div class="w-full h-auto flex flex-col items-center card variant-ghost gap-2 p-2 overflow-y-auto">

                <!-- User Type -->
                <div class="w-full flex flex-col card variant-soft text-center gap-4 p-4">
                    {#if userData.user_type == "admin"}
                        <h1 class="text-3xl card variant-filled-secondary p-2">Admin</h1>
                    {:else if userData.user_type == "employee"}
                        <h1 class="text-3xl card variant-filled-secondary p-2">Employee</h1>
                    {:else if userData.user_type == "customer"}
                        <h1 class="text-3xl card variant-filled-secondary p-2">Customer</h1>
                    {/if}
                </div>
                
                <!-- Profile Icon -->
                <div class="w-full flex justify-center card variant-soft gap-8 p-4">
                    <div class="flex flex-col gap-3 items-center justify-center">
                        <h1 class="text-xl">Profile Picture</h1>
                        <FileButton name="files" class="px-4" accept="image/*">Edit</FileButton>
                    </div>

                    <Avatar initials="JD" background="bg-primary-500" width="w-32" />
                </div>

                <!-- User Name and Email -->
                <div class="w-full flex flex-col items-center card variant-soft text-center gap-3 p-3">
                    <h1 class="w-full text-3xl card variant-ghost rounded-lg p-1">{userData.name}</h1>
                    <h1 class="w-full text-xl card variant-ghost rounded-lg p-2">{userData.email}</h1>
                </div>
            </div>
        
            {#if userOrders && (userData.user_type == "customer" || userData.user_type == "admin")}

                <!-- User Orders -->
                <div class="w-full h-full flex flex-col items-center card variant-ghost gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">My Orders</h1>

                    <!-- Orders -->
                    {#each userOrders as order (order.id)}

                        <OrderInfoCard order={order} showCancelButton={true} />

                    {/each}
                </div>
            
            {/if}
            {#if employeeClaimedOrders && (userData.user_type == "employee" || userData.user_type == "admin")}

                <!-- Employee Claimed Orders -->
                <div class="w-full h-full flex flex-col items-center card variant-ghost gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">Claimed Orders</h1>

                    <!-- Claimed Orders -->
                    {#each employeeClaimedOrders as order (order.id)}

                        <OrderInfoCard order={order} />

                    {/each}
                </div>
            
            {/if}
            {#if users && userData.user_type == "admin"}

                <!-- Recently Registered Users -->
                <div class="w-full h-full flex flex-col items-center card variant-ghost gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">Recently Registered</h1>

                    <!-- Users -->
                    <ul class="w-full space-y-4 p-2">
                        {#each recentlyRegisteredUsers as user (user.id)}

                            <li class="flex items-center justify-between p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover">
                                <span class="text-sm md:text-lg font-medium">{user.id}</span>
                                <span class="text-sm md:text-lg">{user.email}</span>
                                <span class="text-sm md:text-lg">{user.user_type}</span>
                            </li>

                        {/each}
                    </ul>
                </div>

                <!-- Recently Actice Employees -->
                <div class="w-full h-full flex flex-col items-center card variant-ghost gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">Active Employees</h1>

                    <!-- Users -->
                    <ul class="w-full space-y-4 p-2">
                        {#each recentlyActiveUsers as user (user.id)}
                            
                            {#if user.user_type == "employee"}
                                <li class="flex items-center justify-between p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover">
                                    <span class="text-sm md:text-lg font-medium">{user.id}</span>
                                    <span class="text-sm md:text-lg">{user.email}</span>
                                    <span class="text-sm md:text-lg">{user.user_type}</span>
                                </li>
                            {/if}

                        {/each}
                    </ul>
                </div>

                <!-- Recently Placed Orders -->
                <div class="w-full h-full flex flex-col items-center card variant-ghost gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">Recently Placed Orders</h1>

                    <!-- Orders -->
                    {#each recentlyPlacedOrders as order (order.id)}

                        <OrderInfoCard order={order} />

                    {/each}
                </div>
            
            {/if}
        </div>
    </div>
{/if}