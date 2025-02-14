<script>
	import '../app.postcss';
	import { AppBar, LightSwitch, Avatar } from '@skeletonlabs/skeleton';
	import { orderStore } from "$lib/stores/orders";
</script>


<div class="flex flex-col w-full h-full">

	<!-- Header / AppBar -->
	<AppBar padding="p-4 pb-2.5" shadow="shadow" class="flex h-[80px] justify-center">
		
		<!-- Navigation -->
		<svelte:fragment slot="lead">
			<a href="/"><img src="/FT.png" class="w-64 mr-5"></a>
			<div class="flex gap-[20px]">
				<!--<strong class="text-xl uppercase"><a class="hover:text-primary-500 transition-colors duration-300" href="/">Home Page</a></strong> -->
				<strong class="text-xl uppercase"><a class="hover:text-primary-500 transition-colors duration-300" href="/about-us">About Us</a></strong>
				<strong class="text-xl uppercase"><a class="hover:text-primary-500 transition-colors duration-300" href="/catalog">Catalog</a></strong>
			</div>
		</svelte:fragment>

		<!-- User Navigation -->
		<svelte:fragment slot="trail">
			<LightSwitch />
			<!-- Temp Icon Logo -->
<<<<<<< HEAD
			
=======
			<Avatar initials="JD" background="bg-primary-500" width="w-14" />

			<!-- Added: Cart Icon with Items Count -->
			<a href="/orders" 
			class="relative ml-4 w-10 h-10 bg-white text-gray-800 border border-gray-300 flex items-center justify-center rounded-md hover:bg-primary-500 hover:text-white transition-colors duration-300"
			>
			🛒 <!-- Cart Icon -->

			<!-- Cart Counter Badge -->
			{#if $orderStore.length > 0}
				<span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
					{$orderStore.length}
				</span>
			{/if}
			</a>
			<!-- End of Cart Icon Section -->

		</svelte:fragment> 
>>>>>>> origin/catalog
		
	</AppBar>

	<!-- PAGE CONTENT (height is the space under the header (80px)) -->
	<div id="content-container" class="w-full h-[calc(100%-80px)]">
		<slot />
	</div>

</div>
<<<<<<< HEAD

=======
>>>>>>> origin/catalog
