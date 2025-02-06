
<div class="space-y-9 h-full overflow-y-auto">
    <div class="container h-full mx-auto flex justify-center items-center">
        <div class="space-y-9">
            <img class="w-64 mx-auto rounded-full" src="/leo-pics/leo-cropped.png">
            <h1 class="text-7xl">Leo Guerrero</h1>
            <h1 class="text-5xl text-center">About</h1>
            <button class="w-full text-center bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-100 transition-all duration-300 ease-in-out hover:text-black">
                <a href="https://github.com/Leo-guerrero"><i class="fab fa-github"></i> Github</a>
            </button>
            
        </div>
        
    </div>
    <div class="text-center">
        <div class="space-y-8 bg-surface-100 dark:bg-surface-800 max-w-3xl mx-auto p-4 rounded-2xl">
            <p class ="text-xl"> 
                I chose computer science because I have always had an interest in computers. I built my first computer when 
                I was a sophomore in high school so I could play video games. From there that's when my love for computers grew. 
                I then got into video game development, specifically programming, and web development. Through the course project
                I hope to gain better skills in web development, specifically frameworks so I can put it on my resume. I also want 
                to become a better programmer in general especially when it comes to working in teams. 
            </p> 
        </div>
        <br>
        <br>
        
        <div class="card p-4 grid grid-cols-[auto_1fr_auto] gap-4 items-center bg-transparent">
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
        <p class ="text-2xl"> 
            <br>
            {#if num == 1}
                <span>
                    Like I said before I like playing video games. I prefer to play on a Computer.<br>
                    It also looks like the computer I built back when I was a sophomore so it has a<br>
                    special place in my heart!
                </span>
            {:else}
                <span>
                    I love to play souls games, one of my favorite games of all time is Bloodborne <br>
                    although Elden ring is a good game... I think Bloodborne is still better. I also <br>
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



