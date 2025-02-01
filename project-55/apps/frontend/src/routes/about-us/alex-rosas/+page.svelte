
<body class="w-full h-full overflow-y-auto">

    <h1 class="custom-heading">About Me</h1>

    <!-- Profile Image -->
    <!-- svelte-ignore a11y-img-redundant-alt -->
    <img src="/alex-pics/alex.jpg" alt="Profile Picture">
    <div class="center-wrapper">
    <ul>
        <li class="link">
        <a href="https://github.com/AlexCuhh" target="_blank">My GitHub Profile</a>
        </li>
    </ul>
    </div>
    <br>

    <!-- Short Biography -->
    <p class="center-wrapper">
        My name is Alex Rosas and I'm currently a junior working my way to my CS Degree. 
        I've always been interested in technology but ever since a CS class in high 
        school I knew what I wanted to do in the future as a career. I realized that I enjoyed 
        being hands on with technology programming wise. What I would wish to take out from 
        this project is getting experience working with a group, being in charge of completing
        role in the project, and getting gaining more experince working with a virtual machine/terminal.
    </p>

    <!-- Personal Interests Section -->
    <div class="interests">
        <!-- Gym Image -->
        <div>
            <!-- svelte-ignore a11y-img-redundant-alt -->
            <img src="https://cdn.prod.website-files.com/64b773371a8be924f500533b/64b773371a8be924f50053fa_massive-gyms.jpg" alt="Gym Image" style="width: 300px; height: 200px;" class="interest-image">
            <div class="caption"> I enjoy going to the gym because I love challenges and I constantly strive to improve myself both 
                mentally and physically.</div>
        </div>

        <!-- Racing Simulator Image -->
        <div>
            <img src="/alex-pics/simRacing.jpg" alt="Racing Simulator" style="width: 300px; height: 300px;" class="interest-image">
            <div class="caption">I love the thrill of virtual racing, it almost gives you the same experience
                you would get if you drove in real life. I love dirt rally driving especially since it gives you
                almost the same feeling you would get if you were there in person.
            </div>
        </div>
    </div>
</body>


<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }

    h1 {
        text-align: center;
        color: #0077cc;
    }

    img {
        display: block;
        margin: 10px auto;
        width: 250px;
        height: auto;
        border-radius: 12px;
    }

    .interests {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
    }

    .interest-image {
        width: 45%;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    p {
        line-height: 1.6;
    }

    .caption {
        text-align: center;
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }

    .center-wrapper {
        display: flex;
        justify-content: center;  /* Center horizontally */
        align-items: center;      /* Center vertically (if needed) */
        text-align: center;
        /* height: 100vh;            Full viewport height */
    }

    .custom-heading {
        font-size: 40px;
    }

</style>