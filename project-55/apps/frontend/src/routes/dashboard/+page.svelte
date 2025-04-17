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
    <div class="w-full h-full flex flex-col gap-4 items-center ">

        <div class="w-full md:w-3/4 flex flex-col gap-4 items-center pt-4">
            <h1 class="text-5xl">Dashboard</h1>

            <!-- Info Filters -->
            <form class="w-full md:w-3/4 flex gap-16 items-center justify-center">                
                <div class="flex gap-2 items-center">
                    <input class="checkbox" type="checkbox"/>
                    <p>Admin Info</p>
                </div>
                
                <div class="flex gap-2 items-center">
                    <input class="checkbox" type="checkbox"/>
                    <p>Employee Info</p>
                </div>
        
                <div class="flex gap-2 items-center">
                    <input class="checkbox" type="checkbox"/>
                    <p>Customer Info</p>
                </div>
            </form>
        </div>

        <!-- Navigation -->
        <div class="flex flex-col sm:flex-row w-full md:w-3/4 card variant-surface">
            <a href="/auth/order-control" class="w-full block">
                <button class="btn hover:bg-primary-500 w-full text-2xl">Order Control</button>
            </a>
            <a href="/auth/product-control" class="w-full block">
                <button class="btn hover:bg-primary-500 w-full text-2xl">Product Control</button>
            </a>
            <a href="/auth/user-control" class="w-full block">
                <button class="btn hover:bg-primary-500 w-full text-2xl">User Control</button>
            </a>
        </div>

        <!-- Dashboard Grid -->
        <div class="w-full md:w-3/4 grid grid-cols-1 lg:grid-cols-2 grid-rows-[300px_300px] gap-4 pb-4">

            <!-- User Information -->
            <div class="w-full h-[300px] max-h-[300px] flex gap-3 items-center card variant-surface p-4">
                
                <div class="w-full flex flex-col gap-2 items-center text-center">
                    <!-- User Name and Email -->
                    <h1 class="w-full text-3xl rounded-lg">{userData.name}</h1>
                    <h1 class="w-full text-xl rounded-lg">{userData.email}</h1>

                    <!-- User Type -->
                    <div class="w-full flex flex-col text-center pt-8">
                        {#if userData.user_type == "admin"}
                            <h1 class="text-2xl card variant-ringed-primary p-2">Admin</h1>
                        {:else if userData.user_type == "employee"}
                            <h1 class="text-2xl card variant-ringed p-2">Employee</h1>
                        {:else if userData.user_type == "customer"}
                            <h1 class="text-2xl card variant-ringed p-2">Customer</h1>
                        {/if}
                    </div>
                </div>
                
                <!-- Profile Icon -->
                <div class="w-1/2 flex flex-col items-center gap-6">  
                    <Avatar initials="JD" background="bg-primary-500" width="w-32" />
                    <FileButton name="files" class="px-4" accept="image/*">Edit</FileButton>
                </div>

            </div>

            {#if users && userData.user_type == "admin"}

                <!-- Recently Registered Users -->
                <div class="h-[300px] max-h-[300px] flex flex-col items-center card variant-surface gap-2 p-2">
                    <h1 class="text-3xl rounded-lg p-2">Recently Registered</h1>

                    <!-- Users -->
                    <ul class="w-full h-full space-y-4 overflow-y-auto hide-scrollbar card variant-soft p-4">
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
                <div class="w-full h-[300px] max-h-[300px] flex flex-col items-center card variant-surface gap-2 p-2">
                    <h1 class="text-3xl rounded-lg p-2">Active Employees</h1>

                    <!-- Users -->
                    <ul class="w-full h-full space-y-4 overflow-y-auto hide-scrollbar card variant-soft p-4">
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
                <div class="w-full h-[616px] max-h-[616px] flex flex-col items-center card variant-surface gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">Recently Placed Orders</h1>

                    <!-- Orders -->
                    <div class="w-full h-full flex flex-col gap-3 overflow-y-auto hide-scrollbar card variant-soft p-4">
                        {#each recentlyPlacedOrders as order (order.id)}
                            <OrderInfoCard order={order} />
                        {/each}
                    </div>
                </div>
            
            {/if}
            {#if employeeClaimedOrders && (userData.user_type == "employee" || userData.user_type == "admin")}

                <!-- Employee Claimed Orders -->
                <div class="w-full h-[616px] max-h-[616px] flex flex-col items-center card variant-surface gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">Claimed Orders</h1>

                    <!-- Claimed Orders -->
                    <div class="w-full h-full flex flex-col gap-3 overflow-y-auto hide-scrollbar card variant-soft p-4">
                        {#each employeeClaimedOrders as order (order.id)}
                            <OrderInfoCard order={order} showClaimButton={true} />
                        {/each}
                    </div>
                </div>
            
            {/if}
            {#if userOrders && (userData.user_type == "customer" || userData.user_type == "admin")}

                <!-- User Orders -->
                <div class="w-full h-[616px] max-h-[616px] flex flex-col items-center card variant-surface gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">My Orders</h1>

                    <!-- Orders -->
                    <div class="w-full h-full flex flex-col gap-3 overflow-y-auto hide-scrollbar card variant-soft p-4">
                        {#each userOrders as order (order.id)}
                            <OrderInfoCard order={order} showCancelButton={true} />
                        {/each}
                    </div>
                </div>
            
            {/if}
        </div>
    </div>
{/if}