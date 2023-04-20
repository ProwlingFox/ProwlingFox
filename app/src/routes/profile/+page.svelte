<script>
	import { parseJWT, post } from '$lib/requestUtils'
	import { tweened } from 'svelte/motion'
	import { cubicOut } from 'svelte/easing'
	// import { Button } from 'flowbite-svelte'

	let carousel: HTMLElement

	let carouselPosition = tweened(0, {
		duration: 600,
		easing: cubicOut,
	})

	function carouselNext() {
		let { scrollWidth, clientWidth } = carousel
		let maxScrollLeft = scrollWidth - clientWidth

		carouselPosition.update((current) =>
			Math.min(current + clientWidth, maxScrollLeft)
		)

		carouselPosition.subscribe((value) => {
			carousel.scrollLeft = value
		})
	}

	async function setUserData(): Promise<void> {
		const body = {
			name: 'Liaaaaaa',
			tel: '123-456-7890',
			pronouns: 'she/her',
			job_preferences: {
				roles: ['Frontend', 'Backend'],
				sector: 'IT',
				locations: ['New York, New York'],
				remote: true,
				salary: 100000,
			},
		}

		const response = await post('/user/update', body)
		if (response.success) {
			console.log('hi')
		}
	}

	// setUserData()
</script>

<!-- <Button>hi</Button> -->

<div class="carousel flex" bind:this={carousel}>
	<div class="bg-orange-300 h-full">
		<div class="h-full w-full flex items-center justify-center">
			<div class="flex flex-col">
				<div class="m-2 flex flex-col">
					<label for="name" class="">Name</label>
					<input type="text" class="" />
				</div>
				<div class="m-2 flex flex-col">
					<label for="name" class="">Phone number</label>
					<input type="text" class="" />
				</div>
				<div class="m-2 flex flex-col">
					<label for="name" class="">Pronouns</label>
					<input type="text" class="" />
				</div>
				<button
					on:click={carouselNext}
					class="ml-auto p-2 bg-orange-500 rounded">Next</button>
			</div>
		</div>
	</div>
	<div class="bg-orange-200 h-full">
		<div class="h-full w-full flex items-center justify-center">
			<div class="flex flex-col">
				<div class="m-2 flex flex-col">
					<label for="name" class="">Name</label>
					<input type="text" class="" />
				</div>
				<div class="m-2 flex flex-col">
					<label for="name" class="">Phone number</label>
					<input type="text" class="" />
				</div>
				<div class="m-2 flex flex-col">
					<label for="name" class="">Pronouns</label>
					<input type="text" class="" />
				</div>
				<button
					on:click={carouselNext}
					class="ml-auto p-2 bg-orange-500 rounded">Next</button>
			</div>
		</div>
	</div>
	<div class="bg-orange-100 h-full">
		<div class="h-full w-full flex items-center justify-center">
			<div class="flex flex-col">
				<div class="m-2 flex flex-col">
					<label for="name" class="">Name</label>
					<input type="text" class="" />
				</div>
				<div class="m-2 flex flex-col">
					<label for="name" class="">Phone number</label>
					<input type="text" class="" />
				</div>
				<div class="m-2 flex flex-col">
					<label for="name" class="">Pronouns</label>
					<input type="text" class="" />
				</div>
				<button
					on:click={carouselNext}
					class="ml-auto p-2 bg-orange-500 rounded">Next</button>
			</div>
		</div>
	</div>
	<!-- <div class="form">
		<label for="nameInput">
			Name
			<input /><br />
		</label>
	</div> -->
</div>

<style>
	.carousel {
		width: 300vw;
		height: 100%;
		overflow-x: hidden;
	}

	.carousel > div {
		width: 100vw;
		flex-shrink: 0;
	}
</style>
