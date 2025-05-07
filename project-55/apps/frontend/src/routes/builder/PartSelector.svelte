<!-- EDITS AND CHNAGES MADE HERE-->

<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    export let selectedParts;
                                // This is the object that will hold the selected parts 
    //this creates the drop down of all the options for the different parts

    //GPU parts drop down menu
    const gpuOptions = [
      { name: 'Nvidia RTX 3080', model_url: '/models/gpu-RTX.glb' },
      { name: 'NVIDIA RTX 3090 Ti', model_url: '/models/3090RTX.glb' },
      { name: 'VIPERA NVIDIA RTX 4090', model_url: '/models/RTX4090.glb' }   
    ];

    //RAM parts drop down menu
    const ramOptions = [
      { name: 'Corsair Dominator', model_url: '/models/corsair_dominator.glb' },
      { name: 'CORSAIR Vengeance RGB PRO', model_url: '/models/corsairvengeancergbram.glb' },
  ];

    //processor options
    const processorOptions = [
      { name: 'Intel Core i5-7400 Quad-core', model_url: '/models/Intelli5.glb' },
      { name: 'AMD Ryzen7 2700X Processor', model_url: '/models/AMDRyzen72700XProcessor.glb' }
    ];

    const motherboardOptions = [
      { name: 'AsusRogStrixz-390i-gaming', model_url: '/models/asus_rog_strixz_390_i_gaming.glb' }
    ];
  
    // helper to bubble up which dropdown to open
    function open(type) {
      dispatch('open-selector', type);
    }
  </script>
  
  <div class="space-y-4">

  <!-- PARTS SELECTED-->

    <!--Below are the dropdown menus to select the specific type of the desired part-->
    <!-- motherboard-->

    <div>
      <button on:click={() => open('motherboard')}>+ Add motherboard</button>
      <select id="select-motherboard" class="w-full card variant-surface p-2 rounded-lg" bind:value={selectedParts.motherboard}>
        <option disabled selected value={null}>Select motherboard</option>
        {#each motherboardOptions as opt}
          <option value={opt.model_url}>{opt.name}</option>
        {/each}
      </select>
    </div>

     <!-- RAM Selector -->
     <div>
      <button on:click={() => open('ram')}>+ Add RAM</button>
      <select id="select-ram" class="w-full card variant-surface p-2 rounded-lg" bind:value={selectedParts.ram}>
        <option disabled selected value={null}>Select RAM</option>
        {#each ramOptions as opt}
          <option value={opt.model_url}>{opt.name}</option>
        {/each}
      </select>
    </div>
  
    <!-- Processor Selector -->
    <div>
      <button on:click={() => open('processor')}>+ Add processor</button>
      <select id="select-processor" class="w-full card variant-surface p-2 rounded-lg" bind:value={selectedParts.processor}>
        <option disabled selected value={null}>Select processor</option>
        {#each processorOptions as opt}
          <option value={opt.model_url}>{opt.name}</option>
        {/each}
      </select>
    </div>


    <!-- GPU Selector -->
    <div>
      <button on:click={() => open('gpu')}>+ Add GPU</button>
      <select id="select-gpu" class="w-full card variant-surface p-2 rounded-lg" bind:value={selectedParts.gpu}>
        <option disabled selected value={null}>Select GPU</option>
        {#each gpuOptions as opt}
          <option value={opt.model_url}>{opt.name}</option>
        {/each}
      </select>
    </div>
  
   
  </div>


  
  