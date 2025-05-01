<script lang='ts'>

    let thread = {id: 1, user_id: 1, name: 'Thread #4', initial_message_id: 1}
    let messages = [
        {id: 1, user_id: 1, responding_to_id: null, message: 'Hi' },
        {id: 2, user_id: 2, responding_to_id: 1, message: 'Hello' },
        {id: 3, user_id: 1, responding_to_id: 2, message: 'This is a test This is a test This is a test This is a test This is a test This is a test' },
        {id: 4, user_id: 2, responding_to_id: 3, message: 'This is a test' },
        {id: 5, user_id: 1, responding_to_id: 4, message: 'This is a test' },
        {id: 6, user_id: 2, responding_to_id: 5, message: 'This is a test' }
    ];

    let currentMessage = '';

    function handleSubmit() {
        // if (!name || !price || !description || !brand || !options || !product_type || !product_stock) {
        //     toastStore.trigger({
        //         message: 'Required Fields Missing',
        //         background: 'variant-filled-error',
        //     });
        //     return;
        // }

        // if (imageFiles.length === 0 && image_ids.length === 0) {
        //     toastStore.trigger({
        //         message: 'At Least One Image is Required',
        //         background: 'variant-filled-error',
        //     });
        //     return;
        // }

        // dispatch('submit', {
        //     product: {
        //         id,
        //         name,
        //         price,
        //         description,
        //         brand,
        //         options: options.split(',').map((opt) => opt.trim()),
        //         product_type,
        //         product_stock,
        //         hidden,
        //         image_ids: image_ids,
        //         image_urls: image_urls,
        //     },
        //     files: imageFiles
        // });
    }

</script>


<!-- Parent Div, Height of Screen - Header Height -->
<div class="w-full h-[calc(100vh-80px)]">
    <!-- Flex Div -->
    <div class="w-full h-full min-h-96 flex flex-col items-center p-4">

        <!-- Contact Card -->
        <div class="w-full md:w-3/4 h-full min-h-80 flex flex-col items-center card variant-surface p-2">

            <h1 class="h-16 text-3xl rounded-lg p-2">Contact</h1>

            <!-- Inner Card / Message Info -->
            <div class="w-full h-full min-h-64 flex flex-col card variant-soft p-4">

                <!-- Thread Name -->
                <h1 class="w-full text-2xl text-center rounded-lg card variant-surface p-2">{thread.name}</h1>
                
                <!-- Messages -->
                <div class="w-full h-full flex flex-col gap-2 p-4 overflow-y-auto hide-scrollbar">
                    {#each messages as message}

                        {#if message.user_id == 1}

                            <div class="w-full flex justify-end text-center">
                                <div class="w-auto max-w-64 md:max-w-96 p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card">
                                    <span class="text-sm md:text-lg font-medium">{message.message}</span>
                                </div>
                            </div>

                        {:else}

                            <div class="w-full flex justify-start text-center">
                                <div class="w-auto max-w-64 md:max-w-96 p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card">
                                    <span class="text-sm md:text-lg font-medium">{message.message}</span>
                                </div>
                            </div>

                        {/if}

                    {/each}
                </div>

                <!-- Send Message -->
                <form 
                    on:submit|preventDefault={handleSubmit}
                    class="flex gap-2 w-full rounded-lg justify-center text-base-content card variant-surface p-2"  
                >   
                    <!-- Message -->
                    <input
                        id="message-field" 
                        class="input h-[50px] min-h-[30px] focus:outline-none p-2 rounded-lg shadow-lg" 
                        type="text" 
                        placeholder="Enter Message Here"
                        bind:value={currentMessage} 
                        required 
                    />

                    <!-- Submit / Send Message Button -->
                    <button 
                        type="submit"
                        class="w-[150px] h-[50px] btn variant-ghost hover:text-primary-500 font-bold uppercase text-2xl rounded-lg shadow-lg" 
                    >
                        Send
                    </button>
                </form>

            </div>
        </div>
    </div>
</div>