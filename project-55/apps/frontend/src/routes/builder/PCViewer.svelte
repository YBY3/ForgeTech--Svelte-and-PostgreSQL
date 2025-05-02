<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';


  // Shared prop: URLs of the selected part models
  export let selectedParts: {
    cpu: string | null;
    gpu: string | null;
    ram: string | null;
    processor: string | null;
    motherboard: string | null;

  };


// Three.js Core Objects
  let canvas: HTMLCanvasElement;
  let scene: THREEP.Scene;
  let camera: THREE.PerspectiveCamera;
  let renderer: THREE.WebGLRenderer;
  let controls: OrbitControls;
  let loader: GLTFLoader;
//DECIDED TO REMOVE THE MOUNTS SINCE IT WAS CAUSING DIFFICULTIES WITH APPEARING ON THE CASE
//THE MOUNT POINTS ARE STILL ON THE GLB FILE SO THAT CAN BE ADDRESSED LATER
  // // these will point at empty container nodes inside the case that I predefined in my .glb file
  // let cpuMount: THREE.Object3D;
  // let gpuMount: THREE.Object3D;
  // let ramMount: THREE.Object3D;

  //UPDATED

  //this is an object literal that will hold the mount points
  let loadedParts = {
    cpu: null,
    gpu: null,
    ram: null,
    processor: null,
    motherboard: null
  };

  /**
   * loadPart()
   * 1) Centers the part on its own bounding‐box center
   * 2) Scales it so its largest dimension = targetSize
   * 3) Snaps it into the correct mount (cpu, gpu, or ram)
   */
  function loadPart(url: string, type: 'cpu'|'gpu'|'ram' |'processor') {

    //skip if already loaded
    if (loadedParts[type] === url) {
      return;
    }

    //set up the loader

  loader.load(url, gltf => {
    //Remove existing part of this type if it is visible on the case
    //scene is a Three.js property that represents the 3D scene
    //.children is a property of the scene that contains all the objects in the scene that is not its parent
    //this an if statement that checks if the object has a userData property and if it is equal to the type
    scene.children.forEach(obj =>{
      if (obj.userData?.partType === type) scene.remove(obj);
    });

    //set up the part
    const part = gltf.scene;

    // --- prevent shared-material side effects ---
    
    //userData is used to store the type of part that is being loaded 
    //userData is a Three.js property that allows you to attach custom data to an object
    //so part.userDate is an object that contains a property called partType
    //basically this is a way to keep track of what type of part is being loaded onto the case
    part.userData = {partType:type};

    //now we must center the part on a bounding box center
//COMPUTE BOX & SIZE
    //box is a constant this line is creating an instance of the Box3 class
    //the Box3 class is a Three.js class that represents an axis-aligned bounding box in 3D space
    //the setFromObject method is used to calculate the bounding box of the part
    //this is done by passing the part object to the setFromObject method
    //basically this is creating an instance for me to create a box around the part that is being loaded
    const box = new THREE.Box3().setFromObject(part);
    const size   = box.getSize(new THREE.Vector3());
    //this constant maxDim is used to get the size of the part
    //it is not used to set the size of the part
    const maxDim = Math.max(size.x, size.y, size.z);
    //setScalar is used to set the scale of the part using the formula 1/maxDim
    //the scale is set to 1/maxDim so that the largest dimension of the part is equal to 1
//SCALE DOWN TO UNIT
    part.scale.setScalar(1 / maxDim);
// set the size of the different parts,one means remain the same
    const scaleMultiplier = {
      cpu: 1,         
      gpu: 1,
      ram: 1,
      processor: 0.4 ,
      motherboard: 0.7
       
    }[type];
    //this is used to set the scale of the part
    part.scale.multiplyScalar(scaleMultiplier);
    part.updateMatrixWorld(true);

//RECOMPUTER BOX AFTER SCALING
    box.setFromObject(part);
    const center = box.getCenter(new THREE.Vector3());

//SUBTRACT THE CENTER FROM THE PART, THIS PREVENTS IT FROM SHIFTING UNPREDICTABLY
    part.position.sub(center);

    // position on case
    const offset = {
      cpu: new THREE.Vector3(-1.5, 0.5, 0),
      gpu: new THREE.Vector3( 0.04, 0.4, -0.55),
      ram: new THREE.Vector3( 0.2, 0.5, -0.35),
      processor: new THREE.Vector3( .22, 0.84, -0.15),
      motherboard: new THREE.Vector3( 0.15, 0.84, -0.15)
    }[type];
    part.position.add(offset);

    scene.add(part);
    loadedParts[type] = url;
  });
}

  // Load case model
  function loadCase() {
    loader.load('/models/case_with_mounts.glb', (gltf) => {
      const caseModel = gltf.scene;
      
      // Scale and position case
      caseModel.scale.setScalar(2.0);
      
      // Center on floor
      const box = new THREE.Box3().setFromObject(caseModel);
      const minY = box.min.y;
      caseModel.position.y = -minY;
      
      // Add to scene
      scene.add(caseModel);
    });
  }

  // Reactively reload parts when selection changes
  $: selectedParts.cpu && loadPart(selectedParts.cpu, 'cpu');
  $: selectedParts.gpu && loadPart(selectedParts.gpu, 'gpu');
  $: selectedParts.ram && loadPart(selectedParts.ram, 'ram');
  $: selectedParts.processor && loadPart(selectedParts.processor, 'processor');
  $: selectedParts.motherboard && loadPart(selectedParts.motherboard, 'motherboard');

  // Adjust camera & renderer on container resize
  function resize() {
    if (!canvas || !renderer || !camera) return;
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }

  onMount(() => {
    // SCENE & DARK BACKGROUND
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x121212);

    //  CAMERA VIEW - How the case appears on the screen

    // field of view is 100 degrees this means the camera is very close to the object
    //aspect ratio is 1 (width/height) to give a square view
    // near and far planes are 0.1 and 1000 respectively
    camera = new THREE.PerspectiveCamera(100, 1, 0.1, 1000);

    // X, Y and Z coordinates of a camera
    //here x is -2, y is 1 and z is 1
    // the x moves the unit 2 to the left which gives it this slanted angle
    //the y moves it above the grid by 1
    //the z moves it closer to the screen by 1, an increase in number puts it further away
    camera.position.set(-2, 1, 1);

    // Renderer
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    resize();
    
    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    
    // Lighting
    scene.add(new THREE.AmbientLight(0x888888));
    const dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(1, 1, 1);
    scene.add(dirLight);
    
    // Grid
    const grid = new THREE.GridHelper(10, 10);
    scene.add(grid);
    
    // Initialize loader and load case
    loader = new GLTFLoader();
    loadCase();
    
    // Load initial parts if any
    if (selectedParts.cpu) loadPart(selectedParts.cpu, 'cpu');
    if (selectedParts.gpu) loadPart(selectedParts.gpu, 'gpu');
    if (selectedParts.ram) loadPart(selectedParts.ram, 'ram');
    if (selectedParts.processor) loadPart(selectedParts.processor, 'processor');
    if (selectedParts.motherboard) loadPart(selectedParts.motherboard, 'motherboard');
    
    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }
    animate();
    
    // Window resize handler
    window.addEventListener('resize', resize);
  });

  onDestroy(() => {
    window.removeEventListener('resize', resize);
  });
</script>

<style>
  .viewer-container {
    background: #121212;
    border-radius: 0.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    position: relative;
    overflow: hidden;
  }
  
  canvas {
    background-color: #121212 !important;
  }
  
  .footer-text {
    position: absolute;
    bottom: 0.5rem;
    left: 0.75rem;
    color: #888;
    font-size: 0.75rem;
    line-height: 1.1;
  }
</style>

<div class="viewer-container w-full h-[600px]">
  <canvas bind:this={canvas} class="w-full h-full block"></canvas>
  
  <div class="footer-text">
    Accuracy not guaranteed<br />
    3D models by third parties
  </div>
</div>