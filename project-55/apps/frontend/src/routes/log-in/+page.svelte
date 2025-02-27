<script>
    let email = "";
    let password = "";
    let firstName = "";
    let lastName = "";
    let showPassword = false;
    let isLogin = true; // This flag will toggle between Login and Sign-Up form

    const handleLogin = () => {
        // Handle login submission
        console.log("Login submitted", { email, password });
    };

    const handleSignUp = () => {
        // Handle sign-up submission
        console.log("Sign-up submitted", { firstName, lastName, email, password });
    };

    const toggleForm = () => {
        isLogin = !isLogin; // Toggle between forms
    };
</script>

<div>
    <section class="text-center">
        <!-- Background image -->
        <div class="p-5 bg-cover bg-center h-[300px]" style="background-image: url('/login-pics/loginBack.jpg');"></div>

        <!-- Card -->
        <div class="mx-4 md:mx-auto max-w-lg -mt-24 bg-surface-200 dark:bg-surface-700 shadow-lg rounded-lg">
            <div class="py-8 px-6 md:px-10">
                <h2 class="text-3xl font-bold mb-5 text-on-surface">{isLogin ? 'Login' : 'Sign up now'}</h2>

                {#if isLogin}
                    <!-- Login Form -->
                    <form class="space-y-4" on:submit|preventDefault={handleLogin}>
                        <div class="max-w-md mx-auto">
                            <label for="email" class="block text-sm font-medium text-on-surface">Email address</label>
                            <input type="email" id="email" bind:value={email} required
                                class="mt-1 w-full px-2 py-2 border-b border-gray-500 focus:border-primary focus:outline-none bg-transparent text-on-surface placeholder-gray-400" placeholder="Enter Email"/>
                        </div>

                        <div class="max-w-md mx-auto relative">
                            <label for="password" class="block text-sm font-medium text-on-surface">Password</label>
                            <div class="flex items-center border-b border-gray-500">
                                {#if showPassword}
                                    <input id="password" type="text" bind:value={password} required
                                        class="w-full px-4 py-2 bg-transparent focus:outline-none text-on-surface placeholder-gray-400" placeholder="Enter Password"/>
                                {:else}
                                    <input id="password" type="password" bind:value={password} required
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
                                Login
                            </button>
                        </div>
                    </form>

                {:else}
                    <!-- Sign-Up Form -->
                    <form class="space-y-4" on:submit|preventDefault={handleSignUp}>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="max-w-md mx-auto">
                                <label for="firstName" class="block text-sm font-medium text-on-surface">First Name</label>
                                <input type="text" id="firstName" bind:value={firstName} required
                                    class="mt-1 w-full px-2 py-2 border-b border-gray-500 focus:border-primary focus:outline-none bg-transparent text-on-surface" placeholder="Enter First Name"/>
                            </div>

                            <div class="max-w-md mx-auto">
                                <label for="lastName" class="block text-sm font-medium text-on-surface">Last Name</label>
                                <input type="text" id="lastName" bind:value={lastName} required
                                    class="mt-1 w-full px-2 py-2 border-b border-gray-500 focus:border-primary focus:outline-none bg-transparent text-on-surface" placeholder="Enter Last Name"/>
                            </div>
                        </div>

                        <div class="max-w-md mx-auto">
                            <label for="email" class="block text-sm font-medium text-on-surface">Email address</label>
                            <input type="email" id="email" bind:value={email} required
                                class="mt-1 w-full px-2 py-2 border-b border-gray-500 focus:border-primary focus:outline-none bg-transparent text-on-surface" placeholder="Enter Email"/>
                        </div>

                        <div class="max-w-md mx-auto relative">
                            <label for="password" class="block text-sm font-medium text-on-surface">Password</label>
                            <div class="flex items-center border-b border-gray-500">
                                {#if showPassword}
                                    <input id="password" type="text" bind:value={password} required
                                        class="w-full px-4 py-2 bg-transparent focus:outline-none text-on-surface placeholder-gray-400" placeholder="Enter Password"/>
                                {:else}
                                    <input id="password" type="password" bind:value={password} required
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
                {/if}

                <!-- Toggle between Login and Sign-up -->
                <div class="mt-4 text-sm">
                    {#if isLogin}
                        <p>Don't have an account? 
                            <button type="button" on:click={toggleForm} class="text-blue-400 hover:text-light-blue-600">Sign up</button>
                        </p>
                    {:else}
                        <p>Already have an account? 
                            <button type="button" on:click={toggleForm} class="text-blue-400 hover:text-light-blue-600">Log In</button>
                        </p>
                    {/if}
                </div>

            </div>
        </div>
    </section>
</div>
