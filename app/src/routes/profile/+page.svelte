<script>
	import { parseJWT, post } from '$lib/requestUtils'
	import { tweened } from 'svelte/motion'
	import { cubicOut } from 'svelte/easing'
	import PersonalInfoForm from '$components/SignupFlow/PersonalInfoForm.svelte'
	import JobSelectionForm from '$components/SignupFlow/JobSelectionForm.svelte'
	import JobPreferencesForm from '$components/SignupFlow/JobPreferencesForm.svelte'
	import type { User } from '$interfaces/user'

	let carousel: HTMLElement

	let user: User = {
		name: '',
		tel: '',
		pronouns: '',
		job_preferences: {
			roles: [''],
			sector: '',
			locations: [''],
			remote: false,
			salary: 0,
		},
	}

	let carouselPosition = tweened(0, {
		duration: 600,
		easing: cubicOut,
	})

	function carouselNext(): void {
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
	<PersonalInfoForm bind:user {carouselNext} />
	<JobSelectionForm bind:user {carouselNext} />
	<JobPreferencesForm bind:user {carouselNext} />
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
