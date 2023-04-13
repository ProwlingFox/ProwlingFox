<script>
	import { get } from '$lib/requestUtils'
	import { onMount } from 'svelte'
	import JobText from '$components/job/JobText.svelte'
	import Fa from 'svelte-fa/src/fa.svelte'
	import type { Job } from '$interfaces/job'
	import {
		faStairs,
		faGraduationCap,
		faLocation,
	} from '@fortawesome/free-solid-svg-icons'

	export let data

	const jobId = data.jobId

	console.log(jobId)

	let job: Job

	onMount(() => {
		get('/jobs/' + jobId).then((res) => {
			job = res

			console.log(job)

			const min = 50000
			const max = 200000
			const randomNum = Math.floor(Math.random() * (max - min + 1)) + min
			job.salary ||= '$' + randomNum

			// const locations = [
			// 	'Remote',
			// 	'New York, New York',
			// 	'London, England',
			// 	'Atlanta, Georgia',
			// ]
			// job.location =
			// 	locations[Math.floor(Math.random() * locations.length)]

			const experienceLevels = [
				'Junior Level',
				'Mid Level',
				'Senior Level',
				'2 years',
				'4 years',
			]

			job.experience =
				experienceLevels[
					Math.floor(Math.random() * experienceLevels.length)
				]

			const educationLevels = ['Bachelors', 'Masters']

			job.education =
				educationLevels[
					Math.floor(Math.random() * educationLevels.length)
				]

			console.log(job)
		})
	})
</script>

{#if job}
	<div class="w-full sm:p-5">
		<div class="bg-white w-full p-4 sm:rounded-xl">
			<div class="mb-2">
				<h1 class="inline">{job.role},</h1>
				<a class="inline underline" href="#">{job.company.name}</a>
			</div>
			{#if job.location}
				<div>
					<Fa icon={faLocation} class="inline" />
					<span>{job.location}</span>
				</div>
			{/if}

			{#if job.experience}
				<div>
					<Fa icon={faStairs} class="inline" />
					<span>{job.experience}</span>
				</div>
			{/if}
			{#if job.education}
				<div>
					<Fa icon={faGraduationCap} class="inline" />
					<span>{job.education}</span>
				</div>
			{/if}
		</div>
	</div>
{:else}
	<span>loading</span>
{/if}
