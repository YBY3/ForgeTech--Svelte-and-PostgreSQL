<script lang="ts">
    import { afterUpdate} from "svelte";
    import { createEventDispatcher } from "svelte";
    import type { ThreadType } from "$lib/types/ThreadTypes";
    import type { MessageType } from "$lib/types/MessageTypes";

    //Component Data
    export let userID: number;
    export let thread: ThreadType;
    export let messages: MessageType[]; 

    // let thread = {id: 4, user_id: 1, name: 'Thread #4', initial_message_id: 1}
    // let messages = [
    //     {id: 1, thread_id: 4, user_id: 1, responding_to_id: null, message: 'Hi' },
    //     {id: 2, thread_id: 4, user_id: 2, responding_to_id: 1, message: 'Hello' },
    //     {id: 3, thread_id: 4, user_id: 1, responding_to_id: 2, message: 'This is a test This is a test This is a test This is a test This is a test This is a test' },
    //     {id: 4, thread_id: 4, user_id: 2, responding_to_id: 3, message: 'This is a test' },
    //     {id: 5, thread_id: 4, user_id: 1, responding_to_id: 4, message: 'This is a test' },
    //     {id: 6, thread_id: 4, user_id: 2, responding_to_id: 5, message: 'This is a test' }
    // ];

    //Component Elements
    const dispatch = createEventDispatcher();
    let currentMessage = '';
    let messagesContainer: HTMLDivElement;

    //Scoll to Bottom on New Message
    afterUpdate(() => {
        if (messagesContainer && typeof messagesContainer.scrollHeight === 'number') {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    });

    //Send Message
    function handleMessage() {
        if (!currentMessage) {
            return;
        }

        const respondingID = messages.length > 0 ? messages[messages.length - 1].id : null;

        dispatch('sendMessage', {
            message: {
                id: -1,
                thread_id: thread.id,
                user_id: userID,
                respondingID: respondingID,
                message: currentMessage,
            }
        });

        messages = [...messages, {id: -1, thread_id: 4, user_id: 1, responding_to_id: respondingID, message: currentMessage}];
        currentMessage = '';
    }
</script>


{#if messages && thread}
    <!-- Message Card -->
    <div class="w-full md:w-3/4 h-full min-h-80 flex flex-col items-center card variant-surface p-2">

        <h1 class="h-16 text-3xl rounded-lg p-2">Contact</h1>

        <!-- Inner Card / Message Info -->
        <div class="w-full h-full min-h-64 flex flex-col card variant-soft p-4">

            <!-- Thread Name -->
            <h1 class="w-full text-2xl text-center rounded-lg card variant-surface p-2">{thread.name}</h1>
            
            <!-- Messages -->
            <div 
                class="w-full h-full flex flex-col gap-2 p-4 overflow-y-auto hide-scrollbar"
                bind:this={messagesContainer}
            >
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
                on:submit|preventDefault={handleMessage}
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
{/if}