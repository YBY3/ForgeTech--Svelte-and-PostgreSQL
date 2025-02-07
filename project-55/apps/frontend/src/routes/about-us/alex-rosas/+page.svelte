<script>
    function goToWebsite(){
        window.open("https://github.com/AlexCuhh");
    }
    
</script>

<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col items-center text-center mt-5 max-w-3xl mx-auto p-5">
        <div class="text-2xl font-bold mt-2 mb-3">{"About Me"}</div>
    </div>
  <!-- Profile Image -->
  <img src="/alex-pics/alex.jpg" class="w-64 mx-auto rounded-[20px]">
  
  <div class="flex flex-col items-center text-center mt-5 max-w-3xl mx-auto p-5">
    <div class="center-wrapper">
        <button on:click={goToWebsite} class="button">
            Github Account
        </button>
    </div>
    <br>

    <!-- Short Biography -->
    <p class="center-wrapper">
        My name is Alex Rosas and I'm currently a junior working my way to my CS Degree.
        I've always been interested in technology but ever since a CS class in high
        school I knew what I wanted to do in the future as a career. I realized that I enjoyed
        being hands on with technology programming wise. What I would wish to take out from
        this project is getting experience working with a group, being in charge of completing
        a role in the project, and gaining more experience working with a virtual machine/terminal.
    </p>

    <!-- Personal Interests Section -->
    <!-- Gym Image (Permalink image) -->
    <div class="center-images">
        <div>
            <img class="interest-image"  src="https://cdn.prod.website-files.com/64b773371a8be924f500533b/64b773371a8be924f50053fa_massive-gyms.jpg" style="width: 300px; height: 200px;">
            <div class="caption">
                I enjoy going to the gym because I love challenges and I constantly strive to improve myself both mentally and physically.
            </div>
        </div>

        <!-- Racing Simulator Image (Local image) -->
        <div>
            <img class="interest-image" src="/alex-pics/simRacing.jpg" style="width: 300px; height: 300px;">
            <div class="caption">
                I love the thrill of virtual racing; it almost gives you the same experience you would get if you drove in real life. I love dirt rally driving especially since it gives you almost the same feeling you would get if you were there in person.
            </div>
        </div>
    </div>
  </div>
</div>

<style>
  .interest-image {
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-left: 20px;
  }

  .center-images {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 80px;
    margin: 50px 0;
  }

  .center-images img {
    max-width: 300px;
    width: 100%;
    height: auto;
  }
  .button {
    padding: 10px 20px;
    background-color: #49443f;
    color: rgb(255, 255, 255);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 25px;
  }

  .caption {
    text-align: center;
    font-size: 14px;
    color: #d6c5ba;
    margin-top: 5px;
  }

</style>