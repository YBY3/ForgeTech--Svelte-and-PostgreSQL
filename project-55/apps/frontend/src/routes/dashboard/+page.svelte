<script lang="ts">
    import { onMount } from 'svelte';
    import { getToastStore, Avatar, FileButton } from '@skeletonlabs/skeleton';
    import OrderInfoCard from '$lib/components/order/OrderInfoCard.svelte';
    import type { UserType } from '$lib/types/UserTypes.js';
    import type { OrderType } from '$lib/types/OrderTypes';

    //Tailwind Classes
    let navButtonClass = " w-full h-full btn text-md md:text-lg lg:text-xl hover:text-primary-500 font-bold uppercase rounded-lg ";
    let navContainerClass = " w-full grid grid-cols-3 gap-1 items-center justify-center card variant-soft rounded-lg p-1 ";
    let errorCardClass = " flex justify-center text-xl card variant-soft-error rounded-lg p-4 ";
  
    //Data
    export let data;
    let userData: UserType;
    let userOrders: OrderType[];
    let employeeClaimedOrders: OrderType[];
    let users: UserType[]
    let allOrders: OrderType[]

    //Page Elements
    let submitting = false;
    const toastStore = getToastStore();
    let recentlyRegisteredUsers: UserType[];
    let recentlyActiveEmployees: UserType[];
    let recentlyPlacedOrders: OrderType[];
    let adminInfoToggle = true;
    let employeeInfoToggle = true;
    let customerInfoToggle = true;
    let showAdminInfo: boolean = false;
    let showEmployeeInfo: boolean = false;
    let showCustomerInfo: boolean = false;

    //Reactively Update Tailwind Classes
    $: {
        if (showAdminInfo) {
            navContainerClass = " w-full grid grid-cols-3 gap-1 items-center justify-center card variant-soft rounded-lg p-1 ";
        }
        else if (showEmployeeInfo) {
            navButtonClass = " w-full h-full btn text-xl hover:text-primary-500 font-bold uppercase rounded-lg ";
            navContainerClass = " w-full grid grid-cols-2 gap-1 items-center justify-center card variant-soft rounded-lg p-1 ";
        }
    }

    onMount(() => {
        if (data.user != null) {
            if (data.user.success == true) {
                userData = data.user.response;
            }
        }

        if (data.userOrders != null) {
            if (data.userOrders.success == true) {
                if (Array.isArray(data.userOrders.response)) {
                    userOrders = data.userOrders.response;
                }
            }
        }

        if (data.employeeClaimedOrders != null) {
            if (data.employeeClaimedOrders.success == true) {
                if (Array.isArray(data.employeeClaimedOrders.response)) {
                    if (data.employeeClaimedOrders.response.length > 0) {
                        employeeClaimedOrders = data.employeeClaimedOrders.response;
                    }
                }
            }
        }

        if (data.users != null) {
            if (data.users.success == true) {
                if (Array.isArray(data.users.response)) {
                    users = data.users.response;

                    //Sort By Recently Registered
                    recentlyRegisteredUsers = users
                        .sort((a: any, b: any) => new Date(a.registered_by).getTime() - new Date(b.registered_by).getTime())

                    //Sort by Recently Active Employees
                    recentlyActiveEmployees = users
                        .filter((user: UserType) => user.user_type === 'employee')
                        .sort((a: any, b: any) => new Date(b.active_by).getTime() - new Date(a.active_by).getTime())
                }
            }
        }

        if (data.allOrders != null) {
            if (data.allOrders.success == true) {
                if ((Array.isArray(data.allOrders.response))) {
                    allOrders = data.allOrders.response;

                    //Sort by Recently Placed
                    recentlyPlacedOrders = allOrders
                    .sort((a: OrderType, b: OrderType) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
                }
            }
        }

        showAdminInfo = (userData.user_type == "admin");
        showEmployeeInfo = (userData.user_type == "employee" || userData.user_type == "admin");
        showCustomerInfo = (userData.user_type == "customer" || userData.user_type == "admin");
    });

    async function unclaimOrder(orderId: number, orderStatus: string) {
		if (submitting) {
			toastStore.trigger({
				message: 'Already Managing Order Claim, Please Wait',
				background: 'variant-filled-error'
			});
			return;
		}

        // if (orderStatus != "claimed") {
        //     toastStore.trigger({
		// 		message: 'This Order is Not Claimed',
		// 		background: 'variant-filled-error'
		// 	});
		// 	return;
        // }

		try {
			submitting = true;
			const formData = new FormData();
			formData.append("order_id", JSON.stringify(orderId));

			const response = await fetch('?/unclaimOrder', {
				method: 'POST',
				body: formData
			});

			const result = await response.json();
			const parsedResultData = JSON.parse(result.data);
			const success = parsedResultData[parsedResultData[0].success];

			if (success) {
				const successMessage = parsedResultData[parsedResultData[0].message];
				toastStore.trigger({
					message: successMessage,
					background: 'variant-filled-success'
				});

				const orderToMove = employeeClaimedOrders.find((o) => o.id === orderId);
				if (orderToMove) {
					employeeClaimedOrders = employeeClaimedOrders.filter((o) => o.id !== orderId);
					orderToMove.status = "pending";
				}
			} else {
				const errorMessage = parsedResultData[parsedResultData[0].error];
				throw new Error(errorMessage);
			}
		} catch (error) {
			const errorMessage: string = `${error}`;
			toastStore.trigger({
				message: errorMessage,
				background: 'variant-filled-error'
			});
		} finally {
			submitting = false;
		}
	}

</script>


{#if userData}
    <!-- Dashboard -->
    <div class="w-full h-full flex flex-col gap-4 items-center pt-4">

        {#if showEmployeeInfo || showAdminInfo} 
            <div class="w-full md:w-3/4 flex flex-col gap-4 items-center">

                <!-- Navigation -->
                <div class="{navContainerClass}">
                    {#if showAdminInfo} 
                        <a href="/control/user-control" class="w-full block">
                            <button class="{navButtonClass}">User Control</button>
                        </a>
                    {/if}
                    <a href="/control/product-control" class="w-full block">
                        <button class="{navButtonClass}">Product Control</button>
                    </a>
                    <a href="/control/order-control" class="w-full block">
                        <button class="{navButtonClass}">Order Control</button>
                    </a>
                </div>

                <!-- Info Filters -->
                {#if showAdminInfo} 
                    <form class="{navContainerClass}">              
                        <div class="w-full flex gap-2 items-center justify-center p-3 rounded-lg">
                            <input class="checkbox" type="checkbox" bind:checked={adminInfoToggle}/>
                            <p>Admin Info</p>
                        </div>
                        
                        <div class="w-full flex gap-2 items-center justify-center p-3 rounded-lg">
                            <input class="checkbox" type="checkbox" bind:checked={employeeInfoToggle}/>
                            <p>Employee Info</p>
                        </div>
                
                        <div class="w-full flex gap-2 items-center justify-center p-3 rounded-lg">
                            <input class="checkbox" type="checkbox" bind:checked={customerInfoToggle}/>
                            <p>Customer Info</p>
                        </div>
                    </form>
                {/if}
            </div>
        {/if}

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

            {#if showAdminInfo && adminInfoToggle}

                <!-- Recently Registered Users -->
                <div class="h-[300px] max-h-[300px] flex flex-col items-center card variant-surface gap-2 p-2">
                    <h1 class="text-3xl rounded-lg p-2">Recently Registered</h1>

                    <!-- Users -->
                    <ul class="w-full h-full space-y-4 overflow-y-auto hide-scrollbar card variant-soft p-4">
                        {#if recentlyRegisteredUsers}
                            {#each recentlyRegisteredUsers as user (user.id)}

                                <li class="flex items-center justify-between p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover">
                                    <span class="text-sm md:text-lg font-medium">{user.id}</span>
                                    <span class="text-sm md:text-lg">{user.email}</span>
                                    <span class="text-sm md:text-lg">{user.user_type}</span>
                                </li>

                            {/each}
                        {:else}
                            <div class="{errorCardClass}">No Users Found</div>
                        {/if}
                    </ul>
                </div>

                <!-- Recently Active Employees -->
                <div class="w-full h-[300px] max-h-[300px] flex flex-col items-center card variant-surface gap-2 p-2">
                    <h1 class="text-3xl rounded-lg p-2">Active Employees</h1>

                    <!-- Users -->
                    <ul class="w-full h-full space-y-4 overflow-y-auto hide-scrollbar card variant-soft p-4">
                        {#if recentlyActiveEmployees}
                            {#if recentlyActiveEmployees.length > 0}
                                {#each recentlyActiveEmployees as user (user.id)}
                                    <li class="flex items-center justify-between p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover">
                                        <span class="text-sm md:text-lg font-medium">{user.id}</span>
                                        <span class="text-sm md:text-lg">{user.email}</span>
                                        <span class="text-sm md:text-lg">{user.user_type}</span>
                                    </li>
                                {/each}
                            {:else}
                                <div class="{errorCardClass}">No Employees Found</div>
                            {/if}
                        {:else}
                            <div class="{errorCardClass}">Error Loading Employees</div>
                        {/if}
                    </ul>
                </div>

                <!-- Recently Placed Orders -->
                <div class="w-full h-[616px] max-h-[616px] flex flex-col items-center card variant-surface gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">Recently Placed Orders</h1>

                    <!-- Orders -->
                    <div class="w-full h-full flex flex-col gap-3 overflow-y-auto hide-scrollbar card variant-soft p-4">
                        {#if recentlyPlacedOrders}
                            {#each recentlyPlacedOrders as order (order.id)}
                                <OrderInfoCard order={order} />
                            {/each}
                        {:else}
                            <div class="{errorCardClass}">No Orders Found</div>
                        {/if}
                    </div>
                </div>
            
            {/if}
            {#if showEmployeeInfo && employeeInfoToggle}

                <!-- Employee Claimed Orders -->
                <div class="w-full h-[616px] max-h-[616px] flex flex-col items-center card variant-surface gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">Claimed Orders</h1>

                    <!-- Claimed Orders -->
                    <div class="w-full h-full flex flex-col gap-3 overflow-y-auto hide-scrollbar card variant-soft p-4">
                        {#if employeeClaimedOrders}
                            {#each employeeClaimedOrders as order (order.id)}
                                <OrderInfoCard order={order} showClaimButton={true} on:claimRequest={(event) => unclaimOrder(event.detail.orderID, event.detail.orderStatus)} />
                            {/each}
                        {:else}
                            <div class="{errorCardClass}">No Claimed Orders Found</div>
                        {/if}
                    </div>
                </div>
            
            {/if}
            {#if showCustomerInfo && customerInfoToggle}

                <!-- User Orders -->
                <div class="w-full h-[616px] max-h-[616px] flex flex-col items-center card variant-surface gap-2 p-2 row-span-2">
                    <h1 class="text-3xl rounded-lg p-2">My Orders</h1>

                    <!-- Orders -->
                    <div class="w-full h-full flex flex-col gap-3 overflow-y-auto hide-scrollbar card variant-soft p-4">
                        {#if userOrders}
                            {#each userOrders as order (order.id)}
                                <OrderInfoCard order={order} showCancelButton={true} /> <!-- Order Cancel Logic Here -->
                            {/each}
                        {:else}
                            <div class="{errorCardClass}">No Orders Found</div>
                        {/if}
                    </div>
                </div>
            
            {/if}
        </div>
    </div>
{/if}