<script lang="ts">
	import '../app.postcss';
	import { AppBar, LightSwitch, Avatar, type PopupSettings, popup } from '@skeletonlabs/skeleton';
	import { productsStore } from "$lib/stores/ProductsStore";
	import { ordersStore } from "$lib/stores/OrdersStore";
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import '@fortawesome/fontawesome-free/css/all.min.css';
	
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });
	
	//Data (data from backend)
	export let data;

	//Save Product Data in Products Store
	if (data.products) {
		productsStore.set(data.products);
	}	

	let isOpen = false;
	import { initializeStores } from '@skeletonlabs/skeleton';

  	initializeStores();

	const popupClick: PopupSettings = {
	event: 'click',
	target: 'popupClick',
	placement: 'bottom',
	closeQuery: '#will-close'
	};
	const popupClickIcon: PopupSettings = {
		event: 'click',
		target: 'popupClickIcon',
		placement: 'bottom',
		closeQuery: '#will-close_two'
	};
	let showPopup = true;
</script>


<div class="flex flex-col w-full h-full">
	{#if showPopup}
	<div class="w-full bg-primary-500 text-white flex justify-between items-center py-1 text-lg">
		<span class="flex-grow text-center">Save up to 25% on our winter sale!</span>
		<button class="text-white mr-4 z-[3]" on:click={() => showPopup = false}><i class="fa-regular fa-x"></i></button>
	  </div>
	{/if}
	<!-- Header / AppBar -->
	<AppBar padding="p-4 pb-2.5" shadow="shadow" class="flex h-[80px] justify-center">
		
		<!-- Navigation -->
		<svelte:fragment slot="lead">
			<a href="/">
				<img 
				  src="LandingPage-pic/Logo Icon.png" 
				  alt="Logo" 
				  class="w-[70px] mb-[2px] mr-5 block md:hidden" />
				<img 
				  src="/FT.png" 
				  alt="Logo" 
				  class="w-[220px] mb-[2px] mr-5 hidden md:block" />
			  </a>
			<div class="flex gap-[20px]">
				<a class="hover:text-primary-500 transition-colors duration-300 text-xl hidden md:block" href="/catalog">Products</a>
				<a class="hover:text-primary-500 transition-colors duration-300 text-xl hidden md:block" href="/about-us">About Us</a>
			</div>
		</svelte:fragment>

		<!-- User Navigation -->
		<svelte:fragment slot="trail">
			<!-- Menu Button -->
			<button class="btn relative p-2 rounded-md md:hidden" use:popup={popupClickIcon}>
			<i class="fas fa-bars text-2xl block"></i>
			</button>

			<!-- Temp Icon Logo -->
			<button use:popup={popupClick}><Avatar initials="JD" background="bg-primary-500" width="w-14" /></button>

			<div class="card p-4 bg-surface-200 -translate-x-[12%] pointer-events-auto z-[3]" data-popup="popupClick">
				<div class="grid grid-cols-1 gap-2">
				<div class="py-2 flex justify-center" ><LightSwitch /></div>
				<a href="/Account"><button class="btn hover:dark:bg-primary-900 hover:bg-primary-100">Account</button></a>
				<a href="/log-in"><button class="btn hover:dark:bg-primary-900 hover:bg-primary-100">Login</button></a>
				<hr class="border-t w-full mx-auto">
				<button id="will-close" class="btn text-white bg-surface-500 hover:bg-primary-500">Close</button>
				</div>
				<div class="arrow" />
			</div>

			<div class="card p-4 bg-surface-200 -translate-x-[12%] pointer-events-auto z-[3] flex justify-between" data-popup="popupClickIcon">
				<div class="grid grid-cols-1 gap-2">
				<a href="/catalog" class="w-full block"><button class="btn hover:dark:bg-primary-900 hover:bg-primary-100 w-full">Products </button></a>
				<a href="/about-us" class="w-full block"><button class="btn hover:dark:bg-primary-900 hover:bg-primary-100 w-full">About Us</button></a>
				<hr class="border-t w-full mx-auto">
				<button id="will-close_two" class="btn text-white bg-surface-500 hover:bg-primary-500">Close</button>
			</div>
				<div class="arrow" />
			</div>

			<!-- Added: Cart Icon with Items Count -->
			<a href="/orders" 
			class="relative ml-4 w-10 h-10 border-2 border-black dark:border-white flex items-center justify-center rounded-full hover:bg-primary-500 hover:text-white transition-colors duration-300 hover:border-none hover:shadow-[0_0_20px_5px_rgba(212,22,60,0.7)]"
			>
			<i class="fa-solid fa-cart-shopping"></i> <!-- Cart Icon 🛒 -->

			<!-- Cart Counter Badge -->
			{#if $ordersStore.length > 0}
				<span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
					{$ordersStore.length}
				</span>
			{/if}
			</a>
			<!-- End of Cart Icon Section -->

		</svelte:fragment> 
		
	</AppBar>

	<!-- PAGE CONTENT (height is the space under the header (80px)) -->
	<div id="content-container" class="w-full overflow-auto">
		<slot />
	</div>

</div>
