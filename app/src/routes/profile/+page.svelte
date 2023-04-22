<script lang="ts">
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

	function carouselMove(next: boolean): void {
		let { clientWidth } = carousel

		carouselPosition.update((current) =>
			Math.min(current + (next ? clientWidth : -clientWidth))
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

<div class="carousel flex" bind:this={carousel}>
	<PersonalInfoForm bind:user {carouselMove} />
	<JobSelectionForm bind:user {carouselMove} />
	<JobPreferencesForm bind:user {carouselMove} />
</div>

<style>
	.carousel {
		width: 300vw;
		height: 100%;
		overflow-x: hidden;
	}
</style>
