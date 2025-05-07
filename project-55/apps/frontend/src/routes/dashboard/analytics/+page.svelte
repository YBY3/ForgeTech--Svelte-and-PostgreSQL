<script lang="ts">
	import type { ProductType } from "$lib/types/ProductTypes.js";
	import type { UserType } from "$lib/types/UserTypes";
	import { onMount } from "svelte";
    import type { OrderProductType, OrderType } from "$lib/types/OrderTypes.js";
	

    let recentlyActiveUsers: UserType[] = [];
    let userData: UserType;
    let users: UserType[];
    let products: ProductType[];
    let popularProducts: ProductType[] = [];

    let productiveEmployees: UserType[] = [];
    let orders: OrderType[] = [];
    let orderProduct: OrderProductType[] = [];

    
    export let data; 

    onMount(() => {
        if (data.user) {
            userData = data.user;
        }


        if (data.users) {
            users = data.users;

            //Sort by Recently Active
            recentlyActiveUsers = users
				.sort((a: any, b: any) => new Date(b.active_by).getTime() - new Date(a.active_by).getTime()).slice(0,3)
        }


        if (data.orders){

            orders = data.orders
            const orderCounts: Record<number, number> = {};

            // Count how many orders each employee claimed
            for (const order of data.orders) {
                if (order.claimed_by_employee_id !== undefined && order.claimed_by_employee_id !== null) {
                    orderCounts[order.claimed_by_employee_id] = (orderCounts[order.claimed_by_employee_id] || 0) + 1;
                }
            }

            // Filter only employees, sort them by number of orders claimed
            productiveEmployees = users
                .filter(user => user.user_type === "employee")
                .sort((a, b) => {
                    const aCount = orderCounts[a.id] || 0;
                    const bCount = orderCounts[b.id] || 0;
                    return bCount - aCount; // Higher claimed first
                }).slice(0,3);
        } else {console.log("skibidi: orders is not an array", data.orders);}

        if (data.products){
            products = data.products;
            
            
        }

        if (data.orderProduct){
            
            orderProduct = data.orderProduct;

            const productQuantityMap: Record<number, number> = {};

            for (const orderPro of orderProduct) {
                const productId = orderPro.product_id;
                const quantity = orderPro.order_quantity;
                productQuantityMap[productId] = (productQuantityMap[productId] || 0) + quantity;
            }

            const top5ProductIDs = Object.entries(productQuantityMap)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([id, _]) => Number(id));

            // console.log("Top 5 product IDs by total quantity:", top5ProductIDs);

            if (products) {
                popularProducts = top5ProductIDs
                    .map(id => products.find(p => p.id === id))
                    .filter((p): p is ProductType => !!p);
            }
        } else { console.log("AHHAHAH"); }

    });

</script>


<div class="w-full flex justify-center pt-4 pr-4 pl-4">
    <div class="w-full h-16 flex justify-between items-center pl-4 pr-4 card variant-surface rounded-lg">
        <a 
            href="/dashboard"
            class="w-20 h-10 btn variant-ghost hover:text-primary-500 font-bold uppercase text-xl rounded-lg shadow-lg p-2" 
        >
            <i class="fa-solid fa-arrow-left"></i>
        </a>
        <h1 class="h-12 text-2xl md:text-3xl rounded-lg p-2 font-bold">Analytics</h1>
        <div class="w-20"></div> <!-- Spacer -->
    </div>
</div>


<div class="bg-background flex flex-col lg:flex-row items-center scroll-smooth gap-4 p-4">
    <div class="w-full h-[450px] max-h-[450px] flex flex-col items-center card variant-surface gap-2 p-2">
        <h1 class="text-3xl rounded-lg p-2">Active Users</h1>

        <!-- Users -->
        <ul class="w-full h-full space-y-4 overflow-y-auto hide-scrollbar card variant-soft p-4">
            {#each recentlyActiveUsers as user (user.id)}
                    <li class="flex items-center justify-between p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover">
                        <span class="text-sm md:text-lg font-medium">{user.id}</span>
                        <span class="text-sm md:text-lg">{user.email}</span>
                        <span class="text-sm md:text-lg">{user.user_type}</span>
                    </li>
            {/each}
        </ul>
    </div>

    <div class="w-full h-[450px] max-h-[450px] flex flex-col items-center card variant-surface gap-2 p-2">
        <h1 class="text-3xl rounded-lg p-2">Productive Employees</h1>

        <!-- Users -->
        <ul class="w-full h-full space-y-4 overflow-y-auto hide-scrollbar card variant-soft p-4">
            {#each productiveEmployees as user (user.id)}
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
    
    <div class="w-full h-[450px] max-h-[450px] flex flex-col items-center card variant-surface gap-2 p-2">
        <h1 class="text-3xl rounded-lg p-2">Popular Products</h1>
        <ul class="w-full h-full space-y-4 overflow-y-auto hide-scrollbar card variant-soft p-4">
            {#each popularProducts as product (product.id)}
                    <li class="flex items-center justify-between p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover">
                        <span class="text-sm md:text-lg font-medium">{product.id}</span>
                        <span class="text-sm md:text-lg truncate">&nbsp;{product.name}&nbsp;</span>
                        <span class="text-sm md:text-lg">{product.product_type}</span>
                    </li>
            {/each}
        </ul>
    </div>
    

</div>