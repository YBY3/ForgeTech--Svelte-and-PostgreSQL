<script lang='ts'>
	import { onMount} from "svelte";
    import { getToastStore } from '@skeletonlabs/skeleton';
    import type { ActionResult } from '@sveltejs/kit';
    import { deserialize } from '$app/forms';
    import MessageCard from "$lib/components/thread/MessageCard.svelte"
    import type { UserType } from "$lib/types/UserTypes";
    import type { MessageType } from "$lib/types/MessageTypes";
    import type { ThreadType } from "$lib/types/ThreadTypes";

    //Data
    export let data;
    let userData: UserType;
    let threads: ThreadType[] = [];
    let currentMessages: MessageType[] = [];
    let pagination: {current_page: number, per_page: number, total_pages: number, total_threads:2}

    //Load Page Data
    onMount(() => {
        //User Data
        if (data.user) {
            userData = data.user;
        }

        //Thread Data
        if (data.threads) {
            if (data.threads.length > 0) {
                threads = data.threads;
                startingThreadsSize = threads.length;
            }
        }

        //Pagination Data
        if (data.pagination) {
            pagination = data.pagination;
        }
    });

    //Page Elements
    const toastStore = getToastStore();
    let submitting = false;
    let newThreadName: string;
    let currentThread: ThreadType;
    let messageSending = false;
    let startingThreadsSize = 0;

    //Page Views
    let threadsView = true;
    let createNewThreadView = false;
    let openThreadView = false;

    function showThreadView() {
        createNewThreadView = false;
        openThreadView = false;
        threadsView = true;
    }

    function showCreateNewThreadView() {
        openThreadView = false;
        threadsView = false;
        createNewThreadView = true;
    }

    function showOpenThreadView(thread: ThreadType) {
        currentThread = thread;

        createNewThreadView = false;
        threadsView = false;
        openThreadView = true;
    }

    async function goToNextPage(direction: number) {
        // 1 == Up
        // -1 == Down
        let page = pagination.current_page;

        if (threads.length == startingThreadsSize) {
            page = pagination.current_page + direction;
        }
        await getAllThreads(page)
    }

    async function getAllThreads(page: number) {
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'This Page is Submitting Changes, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        }

        //Try Submitting
        try {
            submitting = true;
            const formData = new FormData();
            formData.append('page', JSON.stringify(page));

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/get_all_threads', {
                method: 'POST',
                body: formData
            });

            const result: ActionResult = deserialize(await response.text());

            if (result.type === 'success') {
                if (result.data) {
                    if (result.data) {
                        threads = result.data.threads;
                        pagination = result.data.pagination;
                        startingThreadsSize = threads.length;
                        currentMessages = []
                        newThreadName = "";
                    }
                }
            } 
            else if (result.type === 'failure') {
                if (result.data) {
                    const errorMessage = result.data.error;
                    throw new Error(errorMessage);
                }
                throw new Error("Server Error, Try Again Later");
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

    async function addThread() {
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'This Page is Submitting Changes, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        }

        //Try Submitting
        try {
            submitting = true;
            const formData = new FormData();
            formData.append('name', newThreadName);
            formData.append('user_id', JSON.stringify(userData.id));

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/add_thread', {
                method: 'POST',
                body: formData
            });

            const result: ActionResult = deserialize(await response.text());

            if (result.type === 'success') {
                if (result.data) {
                    const thread = result.data.thread;
                    currentMessages = []
                    newThreadName = "";
                    threads = [...threads, thread];
                    startingThreadsSize = threads.length;
				    showOpenThreadView(thread);
                }
            } 
            else if (result.type === 'failure') {
                if (result.data) {
                    const errorMessage = result.data.error;
                    throw new Error(errorMessage);
                }
                throw new Error("Server Error, Try Again Later");
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

    async function getThreadMessages(thread: ThreadType) {
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'This Page is Submitting Changes, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        }

        //Try Submitting
        try {
            submitting = true;
            const formData = new FormData();
            formData.append('thread_id', JSON.stringify(thread.id));

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/get_thread_messages', {
                method: 'POST',
                body: formData
            });

            const result: ActionResult = deserialize(await response.text());

            if (result.type === 'success') {
                if (result.data) {
                    currentMessages = result.data.messages;
				    showOpenThreadView(thread);
                }
            } 
            else if (result.type === 'failure') {
                if (result.data) {
                    const errorMessage = result.data.error;
                    throw new Error(errorMessage);
                }
                throw new Error("Server Error, Try Again Later");
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

    async function sendMessage(message: MessageType) {
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'This Page is Submitting Changes, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        }

        //Try Submitting
        try {
            submitting = true;
            messageSending = true;
            const formData = new FormData();
            formData.append('thread_id', JSON.stringify(message.thread_id));
            formData.append('user_id', JSON.stringify(userData.id));
            formData.append('responding_to_id', JSON.stringify(message.responding_to_id));
            formData.append('message', message.message);

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/send_message', {
                method: 'POST',
                body: formData
            });

            const result: ActionResult = deserialize(await response.text());

            if (result.type === 'success') {
                if (result.data) {
                    currentMessages = [...currentMessages, result.data.message];
                }
            } 
            else if (result.type === 'failure') {
                if (result.data) {
                    const errorMessage = result.data.error;
                    throw new Error(errorMessage);
                }
                throw new Error("Server Error, Try Again Later");
            }
        
        } catch (error) {
            const errorMessage: string = `${error}`;
			toastStore.trigger({
                message: errorMessage,
                background: 'variant-filled-error'
            });
        } finally {
            messageSending = false
            submitting = false;
        }
    }

    async function resloveThread(thread: ThreadType) {
        //If Already Submitting, Exit
        if (submitting) {
            toastStore.trigger({
                message: 'This Page is Submitting Changes, Please Wait',
                background: 'variant-filled-error'
            });
            return;
        }

        //Try Submitting
        try {
            submitting = true;
            const formData = new FormData();
            formData.append('thread_id', JSON.stringify(thread.id));

			// Log the form data entries for debugging
			// for (const [key, value] of formData.entries()) {
			// 	console.log(`${key}: ${value}`);
			// }
            
            //Post New Form Data
            const response = await fetch('?/resolve_thread', {
                method: 'POST',
                body: formData
            });

            const result: ActionResult = deserialize(await response.text());

            if (result.type === 'success') {
                toastStore.trigger({
                    message: "Thread Resolved",
                    background: 'variant-filled-success'
                });

                //Remove Thread from threads
                threads = threads.filter(t => t.id !== thread.id);
            } 
            else if (result.type === 'failure') {
                if (result.data) {
                    const errorMessage = result.data.error;
                    throw new Error(errorMessage);
                }
                throw new Error("Server Error, Try Again Later");
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


<!-- Parent Div, Height of Screen - Header Height -->
<div class="w-full h-[calc(100vh-80px)]">
    <!-- Flex Div -->
    <div class="w-full h-full min-h-96 flex flex-col items-center p-4">

        {#if threadsView}

            <!-- Threads -->
            <div class="w-full md:w-3/4 h-full min-h-80 flex flex-col items-center card variant-surface p-2">

                <h1 class="h-16 text-2xl md:text-3xl rounded-lg p-2">Threads</h1>

                <!-- Inner Card / Threads Info -->
                <div class="w-full h-full min-h-48 flex flex-col gap-4 card variant-soft p-4 overflow-y-auto hide-scrollbar">

                    <button 
                        class="text-md md:text-lg lg:text-xl font-bold uppercase hover:text-primary-500 p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover"
                        on:click={() => showCreateNewThreadView()}
                    >
                        Create New Thread
                    </button>
                    {#if threads}
                        {#each threads as thread}
                            <div class="w-full flex gap-2 items-center">
                                <button 
                                    class="w-full flex items-center justify-between p-4 dark:bg-surface-700 rounded-lg shadow-md bg-surface-200 card card-hover"
                                    on:click={() => getThreadMessages(thread)}
                                >
                                    <span class="text-sm md:text-lg">{thread.name}</span>
                                    <span class="text-sm md:text-lg font-medium">{thread.username}</span>
                                </button>

                                {#if userData.user_type == "employee" || userData.user_type == "admin"}
                                    <button 
                                        class="w-1/3 h-12 btn text-lg font-bold rounded-lg variant-filled-secondary"
                                        on:click={() => resloveThread(thread)}
                                    >
                                        Resolve
                                    </button>
                                {/if}
                            </div>
                        {/each}
                    {/if}

                </div>

                {#if pagination}
                    <div class="h-16 text-3xl rounded-lg p-2">
                    
                        {#if pagination.total_pages > 1}
                            {#if pagination.current_page != 1}
                                <button 
                                    class="w-20 h-10 btn variant-ghost hover:text-primary-500 font-bold uppercase text-xl rounded-lg shadow-lg p-2" 
                                    on:click={() => goToNextPage(-1)}
                                >
                                    <i class="fa-solid fa-arrow-left"></i>
                                </button>
                            {/if}
                            {#if pagination.current_page != pagination.total_pages}
                                <button 
                                    class="w-20 h-10 btn variant-ghost hover:text-primary-500 font-bold uppercase text-xl rounded-lg shadow-lg p-2" 
                                    on:click={() => goToNextPage(1)}
                                >
                                    <i class="fa-solid fa-arrow-right"></i>
                                </button>
                            {/if}
                        {/if}

                    </div>
                {/if}
            </div>

        {:else if createNewThreadView}

            <!-- Threads -->
            <div class="w-full md:w-3/4 h-full min-h-80 flex flex-col items-center card variant-surface p-2">

                <div class="w-full h-16 flex justify-between items-center pl-4 pr-4 pb-2">
                    <button 
                        class="w-20 h-10 btn variant-ghost hover:text-primary-500 font-bold uppercase text-xl rounded-lg shadow-lg p-2" 
                        on:click={() => showThreadView()}
                    >
                        <i class="fa-solid fa-arrow-left"></i>
                    </button>
                    <h1 class="h-12 text-2xl md:text-3xl rounded-lg p-2">Create New Thread</h1>
                    <div class="w-20"></div> <!-- Spacer -->
                </div>

                <!-- Inner Card / Threads Info -->
                <div class="w-full h-full min-h-64 flex flex-col justify-center card variant-soft p-4">

                    <form 
                        on:submit|preventDefault={addThread}
                        class="flex gap-2 w-full rounded-lg justify-center text-base-content card variant-surface p-2"  
                    >   
                        <!-- Thread Name Input -->
                        <input
                            id="thread-name-field" 
                            class="input h-[50px] min-h-[30px] focus:outline-none p-2 rounded-lg shadow-lg" 
                            type="text" 
                            placeholder="Enter Thread Name"
                            bind:value={newThreadName} 
                            required 
                        />

                        <!-- Create Thread Button -->
                        <button 
                            type="submit"
                            class="w-[150px] h-[50px] btn variant-ghost hover:text-primary-500 font-bold uppercase text-2xl rounded-lg shadow-lg" 
                        >
                            Create
                        </button>
                    </form>

                </div>
            </div>

        {:else if openThreadView}

            <MessageCard 
                showBackButton={true} messageSending={messageSending} userID={userData.id} thread={currentThread} messages={currentMessages}
                on:goBack={showThreadView} on:sendMessage={(event) => sendMessage(event.detail.message)}
            />

        {/if}
    </div>
</div>