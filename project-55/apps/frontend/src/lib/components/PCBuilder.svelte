<!-- <script>
    import PartList from '../components/PartList.svelte';
    import PCViewer from '../components/PCViewer.svelte';
  
    let selectedParts = {
      cpu:     null,
      gpu:     null,
      ram:     null,
      processor: null,
      motherboard: null
    };
  
    const categories = [
      { key: 'cpu',     label: 'CPU' },
      { key: 'gpu',     label: 'GPU' },
      { key: 'ram',     label: 'RAM' },
      { key: 'processor', label: 'Processor' },
      { key: 'motherboard', label: 'motherboard' }
    ];
  </script>
  
  <div class="flex h-full">
    Main 3D viewer
    <div class="flex-1 p-4">
      <h1 class="text-2xl mb-4">🔧 Build Your Custom PC</h1>
      <PCViewer {selectedParts} />
    </div>
  
    Sidebar Part List
    <aside class="w-80 bg-white dark:bg-gray-800 border-l overflow-y-auto p-4">
      <h2 class="text-xl font-semibold mb-4">Parts ListsSS</h2>
      <PartList {categories} bind:selectedParts />
    </aside> -->
  </div>
  