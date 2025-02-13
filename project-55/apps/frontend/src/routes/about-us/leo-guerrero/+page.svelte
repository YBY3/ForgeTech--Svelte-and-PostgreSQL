
<div class="space-y-5 h-full overflow-y-auto ">
    <br>
    <div class="flex flex-col items-center justify-center space-y-9 md:flex-row md:space-x-6">
    
        <div class="flex flex-col items-center space-y-4">
            <img class="w-64 rounded-full" src="/leo-pics/leo-cropped.png">
            <h1 class="text-6xl sm:text-7xl md:text-9xl">Leo Guerrero</h1>
            <h1 class="text-xl sm:text-2xl md:text-4xl text-primary-500">Software Engineer</h1>
            <br>
            <button class="w-40 h-14 bg-transparent border-2 border-black dark:border-2 dark:border-white dark:text-white rounded-full hover:bg-primary-500 transition-all duration-300 ease-in-out hover:shadow-[0_0_20px_5px_rgba(212,22,60,0.7)] hover:border-none">
                <a href="https://github.com/Leo-guerrero"><i class="fab fa-github"></i> Github</a>
            </button>
        </div>
    </div>
    <hr class="border-t border-white w-full w-3/4 mx-auto">

    <h1 class="text-xl text-center text-primary-500">get to know more...</h1>
    <h1 class="text-7xl text-center">About Me</h1>
    <div >
        <div class="space-y-8 bg-surface-100 dark:bg-surface-800 w-full md:w-3/4 mx-auto p-4 rounded-2xl">
            <p class ="text-xl leading-loose"> 
                I chose computer science because I have always had an interest in computers. I built my first computer when 
                I was a sophomore in high school so I could play video games. From there that's when my love for computers grew. 
                I then got into video game development, specifically programming, and web development. Through the course project
                I hope to gain better skills in web development, specifically frameworks so I can put it on my resume. I also want 
                to become a better programmer in general especially when it comes to working in teams. 
            </p> 
        </div>
        <br>
        <br>
        
        <div class="card p-4 grid grid-cols-[auto_1fr_auto] gap-4 items-center bg-surface-100 dark:bg-surface-800 w-full md:w-3/4 mx-auto">
            <!-- Button: Left -->
            <button type="button" class="btn-icon variant-filled" on:click={carouselLeft}>
                <i class="fa-solid fa-arrow-left" />
            </button>
            <!-- Full Images -->
            <div bind:this={elemCarousel} class="mx-auto flex justify-start snap-x snap-mandatory scroll-smooth flex overflow-x-auto overflow-x-hidden max-w-[800px] rounded-xl">
                {#each unsplashIds as unsplashId}
                    <img
                        class="snap-center w-[800px] container-token"
                        src="{unsplashId}"
                        loading="lazy"
                        alt = "joe mama"
                    />

                {/each}
            </div>
            <!-- Button: Right -->
            <button type="button" class="btn-icon variant-filled" on:click={carouselRight}>
                <i class="fa-solid fa-arrow-right" />
            </button>
        </div>
        <br>
        <p class ="text-2xl w-full md:w-3/4 bg-surface-100 dark:bg-surface-800 mx-auto p-4 rounded-2xl leading-loose"> 
            {#if num == 1}
                <span>
                    Like I said before I like playing video games. I prefer to play on a Computer.
                    It also looks like the computer I built back when I was a sophomore so it has a
                    special place in my heart!
                </span>
            {:else}
                <span>
                    I love to play souls games, one of my favorite games of all time is Bloodborne 
                    although Elden ring is a good game... I think Bloodborne is still better. I also 
                    wish it gets a remaster one day. 
                </span>
            {/if}
        </p> 
        <br>
        <br>
    </div>
    
    </div>
    


<script lang="ts">

    import { onMount } from 'svelte';
    import '@fortawesome/fontawesome-free/css/all.min.css';

let num : number = 1;
let elemCarousel: HTMLDivElement;


const unsplashIds = ['/leo-pics/interestOne.jpg', 'https://i0.wp.com/gnofhorror.com/wp-content/uploads/2024/06/hH6Fn5kUuz4UtnEDeBgCfc-1200-80.jpg'];

onMount(() => {
        elemCarousel.scrollLeft = 0;
    });

function carouselLeft(): void {
	const x =
		elemCarousel.scrollLeft === 0
			? elemCarousel.clientWidth * elemCarousel.childElementCount // loop
			: elemCarousel.scrollLeft - elemCarousel.clientWidth; // step left
	elemCarousel.scroll(x, 0);

    console.log(elemCarousel.scrollLeft)
    if (elemCarousel.scrollLeft == 0) {
        num = 2
    } else {
        num = 1
    }
}
					

function carouselRight(): void {
    
	const x =
		elemCarousel.scrollLeft === elemCarousel.scrollWidth - elemCarousel.clientWidth
			? 0 // loop
			: elemCarousel.scrollLeft + elemCarousel.clientWidth; // step right
	elemCarousel.scroll(x, 0);
    console.log(elemCarousel.scrollLeft)

    if (elemCarousel.scrollLeft == 0) {
        num = 2
    } else {
        num = 1
    }
}




</script>



