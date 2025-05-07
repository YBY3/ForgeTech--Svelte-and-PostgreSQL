<!-- <script>
    import { createEventDispatcher } from 'svelte';
    export let categories;
    export let selectedParts;
    const dispatch = createEventDispatcher();
  
    function open(type) {
      dispatch('open-selector', type);
    }
  </script>
  
  <div class="space-y-6">
    {#each categories as { key, label }}
      <div>
        <h3>{label}</h3>
        {#if selectedParts[key]}
          <div class="flex justify-between">
            <span>{selectedParts[key]}</span>
            <button on:click={() => selectedParts[key] = null}>✕</button>
          </div>
        {:else}
          <button on:click={() => open(key)}>+ Add {label}</button>
        {/if}
      </div>
    {/each}
  </div> -->