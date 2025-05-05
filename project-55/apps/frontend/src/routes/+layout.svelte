<script lang="ts">
	import { onMount } from 'svelte';
	import '../app.postcss';
	import '../app.css';
	import { AppBar, LightSwitch, type PopupSettings, popup, Toast } from '@skeletonlabs/skeleton';
	import { ordersStore } from "$lib/stores/OrdersStore";
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import '@fortawesome/fontawesome-free/css/all.min.css';
	import { initializeStores } from '@skeletonlabs/skeleton';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });
  
	export let data;
  
	initializeStores();	
  
	// Layout Elements
	let mounted = false;
	// Default banner state is true, but check localStorage on mount.
	let showClickable = true;
	let isLoggedIn = false;
  
	// Popup Settings
	const menuPopup: PopupSettings = {
		event: 'click',
		target: 'popupClickIcon',
		placement: 'bottom',
		closeQuery: ''
	};

  
	onMount(() => {
		// Check if the winter sale banner was dismissed previously
		if (localStorage.getItem('winterSaleDismissed') === 'true') {
			showClickable = false;
		}
		if (data.user) {
			isLoggedIn = true;
		}

		mounted = true;
	});
  
	// When the user dismisses the banner, persist that choice
	function dismissWinterSale() {
		showClickable = false;
		localStorage.setItem('winterSaleDismissed', 'true');
	}
  
	function logout() { // TEMP logout functionality
		document.cookie = "user=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
		window.location.href = '/auth/login';
	}
</script>
  
<Toast position="tr" />
  
{#if mounted}
	<div class="flex flex-col w-full h-full">
		<!-- Winter Sale Banner: Only shows if not dismissed -->
		{#if showClickable}
			<div class="w-full bg-primary-500 text-white flex justify-between items-center py-1 text-lg">
				<span class="flex-grow text-center">Save up to 25% on our spring sale!</span>
				<button class="text-white mr-4 z-[3]" on:click={dismissWinterSale}>
					<i class="fa-regular fa-x"></i>
				</button>
			</div>
		{/if}
  
		<!-- Header / AppBar -->
		<AppBar padding="p-4 pb-2.5" shadow="shadow" class="flex h-[80px] justify-center">
			<!-- Navigation -->
			<svelte:fragment slot="lead">
				<a href="/">
					<img 
						src="/forgetech_logos/small.png"
						alt="Small Logo" 
						class="w-[70px] mb-[2px] mr-5 block md:hidden" />
					<img 
						src="/forgetech_logos/large.png" 
						alt="Large Logo" 
						class="w-[220px] mb-[2px] mr-5 hidden md:block" />
				</a>
			</svelte:fragment>
  
			<!-- User Navigation -->
			<svelte:fragment slot="trail">
				<div class="flex items-center gap-4 pl-4 pr-4 pt-2 pb-2 rounded-lg">
					<!-- Menu Button -->
					<button class="btn relative p-2 rounded-md" use:popup={menuPopup}>
						<i class="fas fa-bars text-2xl block"></i>
					</button>
  
					<!-- Shopping Cart Button -->
					<a class="relative group" href="/orders" >
						<button 
						  class="w-10 h-10 border border-2 border-black dark:border-white rounded-md flex items-center justify-center hover:bg-primary-500 transition hover:border-none hover:shadow-[0_0_20px_5px_rgba(212,22,60,0.7)] disabled:opacity-50 disabled:cursor-not-allowed"
						  disabled={!isLoggedIn}
						>
						<i class="fa-solid fa-cart-shopping"></i>
						</button>

						<!-- Counter -->
						{#if $ordersStore.length > 0}
							<span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
								{$ordersStore.length}
							</span>
						{/if}
				
						<!-- Tooltip Below -->
						<span class="absolute left-1/2 -translate-x-1/2 translate-y-1/3 bg-black text-white text-sm px-3 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
						  {#if isLoggedIn}
							  View Cart
						  {:else}
							  Login 
						  {/if}
						</span>
					</a>
				</div>
  
				<!-- Menu Popup: Hidden by default using the "hidden" class.
				     The Skeleton popup directive should remove the hidden class when triggered. -->
				<div class="card p-4 bg-surface-200 -translate-x-[12%] pointer-events-auto z-[3] flex justify-between hidden" data-popup="popupClickIcon">
					<div class="grid grid-cols-1 gap-1">
						<div class="py-2 flex justify-center"><LightSwitch /></div>
						<hr class="border-t w-full mx-auto">
						{#if isLoggedIn}
							<!-- Common Link -->
							<a href="/dashboard" class="w-full block">
								<button class="btn hover:bg-primary-500 w-full">Dashboard</button>
							</a>
					
							<!-- Conditional link based on user_type -->
							{#if data.user}
								{#if data.user.user_type === 'customer' || data.user.user_type === 'admin'}
									<a href="/catalog" class="w-full block">
										<button class="btn hover:bg-primary-500 w-full">Catalog</button>
									</a>
									<a href="/builder" class="w-full block">
										<button class="btn hover:bg-primary-500 w-full">Build A PC</button>
									</a>
								{/if}
								<a href="/threads" class="w-full block">
									<button class="btn hover:bg-primary-500 w-full">Threads</button>
								</a>
							{/if}
							<!-- Always show About Us -->
							<a href="/about-us" class="w-full block">
								<button class="btn hover:bg-primary-500 w-full">About Us</button>
							</a>
							<hr class="border-t w-full mx-auto">
							<div class="pt-2">
								<button on:click={logout} class="btn w-full text-white bg-primary-500">Logout</button>
							</div>
						{:else}
							<a href="/catalog" class="w-full block">
								<button class="btn hover:bg-primary-500 w-full">Products</button>
							</a>
							<a href="/about-us" class="w-full block">
								<button class="btn hover:bg-primary-500 w-full">About Us</button>
							</a>
							<a class="btn hover:bg-primary-500 w-full" href="/auth/login">Login</a>
							<a class="btn hover:bg-primary-500 w-full" href="/auth/sign-up">Sign Up</a>
						{/if}				
					</div>
				</div>
			</svelte:fragment>
		</AppBar>
  
		<!-- PAGE CONTENT (height is the space under the header) -->
		<div id="content-container" class="w-full overflow-auto">
			<slot />
		</div>
	</div>
{/if}
