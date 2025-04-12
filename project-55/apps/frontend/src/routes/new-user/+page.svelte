<script lang="ts">
    import { invalidate } from '$app/navigation';
	import { getToastStore } from '@skeletonlabs/skeleton';

	//Form Data
	let form: HTMLFormElement;


    let showPassword = false;
	let submitting = false;


    const toastStore = getToastStore();

	async function handleSignUp(event: SubmitEvent) {
        //Prevent Default Submission
        event.preventDefault();
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'Already creating user, Please Wait',
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
            const response = await fetch('?/createUser', {
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
                window.location.href = '/user-manager';
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


<div class="p-5 bg-cover bg-center h-[300px]" style="background-image: url('/login-pics/loginBack.jpg');"></div>

<div class="p-4">
	<div class="mx-4 md:mx-auto max-w-lg -mt-48 bg-surface-200 dark:bg-surface-700 shadow-lg rounded-lg">
		<div class="py-8 px-6 md:px-10">
			<h2 class="text-3xl font-bold mb-5 text-on-surface text-center">Create New User</h2>
            <form method="POST" bind:this={form} on:submit={handleSignUp} autocomplete="off" class="space-y-6">
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
                        type="text"
                        pattern="[^@\s]+@[^@\s]+\.[^@\s]+"
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
                            {#if showPassword}
                                <i class="fa-solid fa-eye"></i>
                            {:else}
                                <i class="fa-solid fa-eye-slash"></i>
                            {/if}
                        </button>
                    </div>
                </div>

                <div class="max-w-md mx-auto">
                    <label for="usertype" class="block text-sm font-medium text-on-surface">User Type</label>
                    <div class="mt-2 space-y-2">
                        <label class="flex items-center space-x-2">
                            <input type="radio" name="usertype" value="admin" class="form-radio text-primary" required/>
                            <span>Admin</span>
                        </label>
                        <label class="flex items-center space-x-2">
                            <input type="radio" name="usertype" value="employee" class="form-radio text-primary" required/>
                            <span>Employee</span>
                        </label>
                        <label class="flex items-center space-x-2">
                            <input type="radio" name="usertype" value="customer" class="form-radio text-primary" required/>
                            <span>Customer</span>
                        </label>
                    </div>
                </div>

                <div class="flex gap-10px justify-between gap-x-10">
                    <div>
                        <a href="/user-manager"><button class="px-10 py-2 rounded-lg border-2 border-primary-700 hover:bg-primary-700 transition-all duration-300 transform hover:scale-105 text-center hover:text-white">
                            <i class="fa-solid fa-x"></i> Cancel
                        </button></a>
                    </div>
                    <div>
                        <button type="submit"
                            class="px-10 py-2 rounded-lg border-2 border-secondary-500 hover:bg-secondary-500 transition-all duration-300 transform hover:scale-105 text-center hover:text-white">
                            <i class="fa-solid fa-user-plus"></i> Create
                        </button>
                    </div>
                </div>

            </form>
        </div>
    </div>
</div>