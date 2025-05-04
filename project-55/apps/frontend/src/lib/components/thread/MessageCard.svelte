<script lang="ts">
    import { afterUpdate} from "svelte";
    import { createEventDispatcher } from "svelte";
    import type { ThreadType } from "$lib/types/ThreadTypes";
    import type { MessageType } from "$lib/types/MessageTypes";

    //Component Data
    export let userID: number;
    export let thread: ThreadType;
    export let messages: MessageType[]; 
    export let showBackButton = false;
    export let messageSending = false;

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

    function goBack() {
        dispatch('goBack');
    }

    //Send Message
    function handleMessage() {
        if (messageSending) {return}

        messageSending = true

        if (!currentMessage) {
            return;
        }

        let respondingID = null;
        if (messages.length > 0) {
            respondingID = messages[messages.length - 1].id
        }

        dispatch('sendMessage', {
            message: {
                id: -1,
                thread_id: thread.id,
                user_id: userID,
                responding_to_id: respondingID,
                message: currentMessage,
            }
        });

        messages = [...messages, {id: -1, thread_id: thread.id, user_id: userID, responding_to_id: respondingID, message: 'SENDING...'}];
        currentMessage = '';
    }
</script>


{#if messages && thread}
    <!-- Message Card -->
    <div class="w-full md:w-3/4 h-full min-h-80 flex flex-col items-center card variant-surface p-2">

        <div class="w-full h-16 flex justify-between items-center pl-4 pr-4 pb-2">
            {#if showBackButton}
                <button 
                    class="w-20 h-10 btn variant-ghost hover:text-primary-500 font-bold uppercase text-xl rounded-lg shadow-lg p-2" 
                    on:click={() => goBack()}
                >
                    <i class="fa-solid fa-arrow-left"></i>
                </button>
            {:else}
                <div class="w-20"></div> <!-- Spacer -->
            {/if}
            <h1 class="h-12 text-2xl md:text-3xl rounded-lg p-2">Messages</h1>
            <div class="w-20"></div> <!-- Spacer -->
        </div>

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

                    {#if message.user_id == userID}

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