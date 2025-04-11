<script lang="ts">
    import { invalidate } from '$app/navigation';
    import { getToastStore } from '@skeletonlabs/skeleton';

    // Form Data
    let form: HTMLFormElement;

    // Form Elements
    let showPassword = false;
    let submitting = false;
    const toastStore = getToastStore();

    async function handleLogin(event: SubmitEvent) {
        // Prevent Default Submission
        event.preventDefault();
        // If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'Already Logging In, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        } else if (!form.checkValidity()) {
            return;
        }

        try {
            submitting = true;
            const formData = new FormData(form);

            // Post New Form Data
            const response = await fetch('?/login', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            const parsedResultData = JSON.parse(result.data);
            const success = parsedResultData[parsedResultData[0].success];

            if (success) {
                // Reload App
                invalidate('app:load');
                // Go to Profile page
                window.location.href = '/profile';
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

<div class="text-center">
    <!-- Background image -->
    <div class="p-5 bg-cover bg-center h-[300px]" style="background-image: url('/login-pics/loginBack.jpg');"></div>

    <!-- Login Card -->
    <div class="mx-4 md:mx-auto max-w-lg -mt-24 bg-surface-200 dark:bg-surface-700 shadow-lg rounded-lg">
        <div class="py-8 px-6 md:px-10">
            <h2 class="text-3xl font-bold mb-5 text-on-surface">Login</h2>

            <!-- Login Form -->
            <form method="POST" bind:this={form} on:submit={handleLogin} autocomplete="off" class="space-y-4">
                <div class="max-w-md mx-auto">
                    <label for="email" class="block text-sm font-medium text-on-surface">Email address</label>
                    <input type="email" id="email" name="email" required 
                        class="mt-1 w-full px-2 py-2 border-b border-gray-500 focus:border-primary focus:outline-none bg-transparent text-on-surface placeholder-gray-400" placeholder="Enter Email"/>
                </div>

                <div class="max-w-md mx-auto relative">
                    <label for="password" class="block text-sm font-medium text-on-surface">Password</label>
                    <div class="flex items-center border-b border-gray-500">
                        <!-- Single input element with dynamic type -->
                        <input id="password" 
                               type={showPassword ? "text" : "password"}
                               required
                               name="password"
                               class="w-full px-4 py-2 bg-transparent focus:outline-none text-on-surface placeholder-gray-400" 
                               placeholder="Enter Password"/>
                        <button type="button" 
                                on:click={() => showPassword = !showPassword}
                                class="ml-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-white transition">
                            {showPassword ? "Hide Password" : "Show Password"}
                        </button>
                    </div>
                </div>

                <div class="max-w-md mx-auto">
                    <button type="submit"
                        class="bg-gray-800 text-white px-4 py-2 rounded-lg shadow-md hover:bg-red-600 transition-all duration-300 transform hover:scale-105">
                        Login
                    </button>
                </div>
            </form>

            <!-- Redirect to Sign-up -->
            <div class="mt-4 text-sm">
                <p>
                    Don't have an account? 
                    <a href="/auth/sign-up" class="text-blue-400 hover:text-light-blue-600">
                        Sign up
                    </a>
                </p>
            </div>
        </div>
    </div>
</div>
