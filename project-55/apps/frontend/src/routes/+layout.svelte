<script>
	import '../app.postcss';
	import { AppBar, LightSwitch, Avatar } from '@skeletonlabs/skeleton';
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
			</div>
		</svelte:fragment>

		<!-- User Navigation -->
		<svelte:fragment slot="trail">
			<LightSwitch />
			<!-- Temp Icon Logo -->
			<Avatar initials="JD" background="bg-primary-500" width="w-14" />	
		</svelte:fragment>
		
	</AppBar>

	<!-- PAGE CONTENT (height is the space under the header (80px)) -->
	<div id="content-container" class="w-full h-[calc(100%-80px)]">
		<slot />
	</div>

</div>

