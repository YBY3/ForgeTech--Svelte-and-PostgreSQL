<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { getToastStore } from '@skeletonlabs/skeleton';

	//Form Data
	let form: HTMLFormElement;

	//Form Elements
	let showPassword = false;
	let submitting = false;
	const toastStore = getToastStore();

	async function handleSignUp(event: SubmitEvent) {
        //Prevent Default Submission
        event.preventDefault();
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'Already Signing Up, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        }
        //Checks if Form is Valid / Filled Out Required Items
        else if (!form.checkValidity()) return;

        //Try Submitting
        try {
            submitting = true;
            const formData = new FormData(form);

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/signup', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
			const parsedResultData = JSON.parse(result.data);
            const success = parsedResultData[parsedResultData[0].success];

            if (success) {
				//Reload App
				invalidate('app:load');
				//Go to Catalog
                window.location.href = '/catalog';
            }
            else {
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


<!-- Background image -->
<div class="p-5 bg-cover bg-center h-[300px]" style="background-image: url('/login-pics/loginBack.jpg');"></div>

<!-- Form Card -->
<div class="p-4 text-center">
	<div class="mx-4 md:mx-auto max-w-lg -mt-48 bg-surface-200 dark:bg-surface-700 shadow-lg rounded-lg">
		<div class="py-8 px-6 md:px-10">
			<h2 class="text-3xl font-bold mb-5 text-on-surface">Sign Up</h2>

			<!-- Sign-Up Form -->
			<form method="POST" bind:this={form} on:submit={handleSignUp} autocomplete="off" class="space-y-4">
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div class="max-w-md mx-auto">
						<label for="firstName" class="block text-sm font-medium text-on-surface">First Name</label>
						<input 
							type="text" 
							id="firstName" 
							name="firstName"
							required
							class="mt-1 w-full px-2 py-2 border-b border-gray-500 focus:border-primary focus:outline-none bg-transparent text-on-surface" placeholder="Enter First Name"
						/>
					</div>

					<div class="max-w-md mx-auto">
						<label for="lastName" class="block text-sm font-medium text-on-surface">Last Name</label>
						<input 
							type="text" 
							id="lastName" 
							name="lastName"
							required
							class="mt-1 w-full px-2 py-2 border-b border-gray-500 focus:border-primary focus:outline-none bg-transparent text-on-surface" placeholder="Enter Last Name"
						/>
					</div>
				</div>

				<div class="max-w-md mx-auto">
					<label for="email" class="block text-sm font-medium text-on-surface">Username</label>
					<input 
						type="text" 
						id="userName" 
						name="userName"
						required
						class="mt-1 w-full px-2 py-2 border-b border-gray-500 focus:border-primary focus:outline-none bg-transparent text-on-surface" placeholder="Enter Username"
					/>
				</div>

				<div class="max-w-md mx-auto">
					<label for="email" class="block text-sm font-medium text-on-surface">Email address</label>
					<input 
						type="email" 
						id="email" 
						name="email"
						required
						class="mt-1 w-full px-2 py-2 border-b border-gray-500 focus:border-primary focus:outline-none bg-transparent text-on-surface" placeholder="Enter Email"
					/>
				</div>

				<div class="max-w-md mx-auto relative">
					<label for="password" class="block text-sm font-medium text-on-surface">Password</label>
					<div class="flex items-center border-b border-gray-500">
						{#if showPassword}
							<input id="password" type="text" required name="password"
								class="w-full px-4 py-2 bg-transparent focus:outline-none text-on-surface placeholder-gray-400" placeholder="Enter Password"/>
						{:else}
							<input id="password" type="password" required name="password"
								class="w-full px-4 py-2 bg-transparent focus:outline-none text-on-surface placeholder-gray-400" placeholder="Enter Password"/>
						{/if}
						<button type="button" on:click={() => showPassword = !showPassword}
							class="ml-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-white transition">
							{showPassword ? "Hide Password" : "Show Password"}
						</button>
					</div>
				</div>

				<div class="max-w-md mx-auto">
					<button type="submit"
						class="bg-gray-800 text-white px-4 py-2 rounded-lg shadow-md hover:bg-red-600 transition-all duration-300 transform hover:scale-105">
						Sign up
					</button>
				</div>
			</form>
		</div>
	</div>
</div>