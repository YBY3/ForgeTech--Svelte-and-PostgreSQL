<script>
  import PartSelector from './PartSelector.svelte';
  import PCViewer     from './PCViewer.svelte';
  import PartList     from './PartList.svelte';

  // Now only these three match exactly what your viewer supports:
  let selectedParts = { cpu: null, gpu: null, ram: null, processor: null};
  const categories = [
    { key: 'gpu',     label: 'GPU'     },
    { key: 'ram',     label: 'RAM'     },
    { key: 'processor',     label: 'Processor'     }
  ];

  function handleOpenSelector(e) {
    const el = document.getElementById(`select-${e.detail}`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' }), el.focus();
  }
</script>
<!-- this sets the background, it is black -->
<div class="flex h-screen">
  <div class="w-64 border-r p-4 overflow-auto">
    <h2>Select Parts</h2>
    <PartSelector bind:selectedParts on:open-selector={handleOpenSelector} />
      
  </div>

  <div class="flex-1 p-4">
    <h1>ForgeTech's 3D Builder</h1>
    <h2>Build Your Computer Here Before you Buy!</h2>
    <PCViewer {selectedParts} />
  </div>

</div>
