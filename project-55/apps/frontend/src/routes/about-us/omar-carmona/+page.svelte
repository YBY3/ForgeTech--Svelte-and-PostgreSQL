<script>
	let profilePicture = "/omar-pics/ProfilePicture-cropped.png"; // Replace with your actual profile picture filename in static folder
	let localInterestImage = "/omar-pics/Dune.jpg"; // Image stored locally
	let onlineInterestImage = "https://t4.ftcdn.net/jpg/02/57/33/93/360_F_257339302_LWVM6ZkukZUoVVo8CY0UHx5y283PG9RR.jpg"; // Replace with a real online image URL
</script>
  
<div class="flex flex-col items-center about-me w-full h-full overflow-y-auto">
	<!-- Profile Picture -->
	 <br>
	<img src={profilePicture} alt="Profile Picture" width="200" class="rounded-full" />
	<br>
	<h1 class="text-4xl sm:text-5xl md:text-6xl text-center">Omar Alexander Carmona Rodriguez</h1>
	<br>
	<ul>
		<li class="link">
			<button class="w-40 h-14 bg-transparent border-2 border-black dark:border-2 dark:border-white dark:text-white rounded-full hover:bg-primary-500 transition-all duration-300 ease-in-out hover:shadow-[0_0_20px_5px_rgba(212,22,60,0.7)] hover:border-none"><a href="https://github.com/omarRdgz11" target="_blank"><i class="fab fa-github"></i> GitHub</a></button>
		</li>
	</ul>

	<br/>
	<hr class="border-t border-white w-full w-3/4 mx-auto">

    <h1 class="text-xl text-center text-primary-500">get to know more...</h1>
    <h1 class="text-7xl text-center">About Me</h1>
	<!-- Short Biography -->
	<br>
	<div class="space-y-8 bg-surface-100 dark:bg-surface-800 w-full md:w-3/4 mx-auto p-4 rounded-2xl">
	<p class ="text-xl leading-loose">
	  Hello, my name is Omar Alexander Carmona Rodriguez. I am from Santa Fe New Mexico and I have been at St. Edward's University for the past three years as a computer science major.
	  My interest in the field stems from a fascination of design, I've always been captivated by the process of bringing a project to life. From the early designs, to 
	  prototypes, to polishing, and then the product standing in front of you.
	</p>
	
	<p class ="text-xl leading-loose">
		I've never been the most creative or artistic person, but the process of creation is something that I see
		and apply to multiple apsects of my life, from crocheting, to piano, and now to computer science. Which is what I'm most excited about this class, to bring a bigger scale project 
		into fruition over time and taking the time to really delve into the different processes that happen over the course of starting and finishing a product. 
	</p>
	</div>
	<!-- Personal Interests -->
	<h1 class="text-7xl text-center">My Interests</h1>
	<br>
	<div class="interests flex flex-col items-center w-full">
		<img src={localInterestImage} alt="Local Interest" width="300" />
		<br/>
		<p class ="text-2xl w-full md:w-3/4 bg-surface-100 dark:bg-surface-800 mx-auto p-4 rounded-2xl leading-loose">I am a huge fan of the Dune series, both the novels and the movies. The way it seamlessly explores themes of religion, politics, determinism, faith, ecology, and many more, has always 
			been so captivating to me. And the world building is unlike anything I have experienced before. Very spectacular novel. 
		</p>
		<img src={onlineInterestImage} alt="Online Interest" width="300" />
		<br/>
		<p class ="text-2xl w-full md:w-3/4 bg-surface-100 dark:bg-surface-800 mx-auto p-4 rounded-2xl leading-loose">
		  I am a self taught pianist, it all started one day when I heard a pretty melody on the radio. In that instance this overwhelming feeling of wanting to play that same tune instantly overtook me. 
		  And since then I have been playing the instrument. I am by no means an expert, but I am able to play songs that truly capture me. 
		</p>
		<br/>
	</div>
  </div>