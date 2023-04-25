<script lang="ts">
	import { goto } from '$app/navigation'
	import type { Application as JobApplication } from '$interfaces/application'
	import type { Job } from '$interfaces/job'

	import { applications as as, popNextJobID, jobQueue } from '$lib/myJobs'
	import { get, post } from '$lib/requestUtils'
	import JobApplicationForm from './JobApplicationForm.svelte'

	export let srcJob: Job

	const { send } = $as
	let relatedApplication: JobApplication | undefined

	$: relatedApplication = $as.applications.find(x => x.job_id == srcJob._id)

	$: console.log(relatedApplication)

	$: console.log(srcJob)

	let nextId: string

	let visible = true



	async function apply() {
		post(`/jobs/${srcJob._id}/mark`, { requestApply: true })
		as.update((a) => {
			return {
				applications: [
					{
						_id: srcJob._id,
						job_id: srcJob._id,
						job: srcJob,
						application_read: true,
						application_requested: true,
						application_processing: false,
						application_processed: false,
						progress: {
							label: 'Pending',
							percent: 33,
							color: 'bg-orange-800',
						},
					},
					...a.applications,
				],
				send: $as.send,
				receive: $as.receive,
			}
		})
		visible = false

		//Rlly ugly solution this code should actually preload, the next job in the background like it's allready doing and then fade it in,
		// using goto just to officially change the url like the whole thing is supposed to work in the first place
		setTimeout(loadNext, 2001)
	}

	async function preLoadNext() {
		nextId = await popNextJobID()
		get('/jobs/' + nextId) // Fix so it doesn't duplicate this request lol :3
	}

	async function loadNext() {
		await goto('/jobs/' + (await nextId))
		visible = true
		preLoadNext()
	}

	function reject() {
		post(`/jobs/${srcJob._id}/mark`, { requestApply: false })
		//Discard Animation
		//Load New
		loadNext()
	}

	preLoadNext()
</script>

{#if visible}
<div class="flex relative {"left-2"}">
	<div id="card" out:send={{ key: srcJob._id }}>
		{#if relatedApplication?.application_processed}
			<div id="banner" class="bg-green-400">
				Application Ready For Review
			</div>
		{:else if relatedApplication?.application_processing}
			<div id="banner" class="bg-orange-400">
				Application Processing
			</div>
		{:else if relatedApplication?.application_requested}
			<div id="banner" class="bg-orange-400">
				Application in Queue
			</div>
		{/if}
		<div class="flex justify-center">
			<img src={srcJob.company.logo} alt="" />
		</div>

		<h1 class="mt-4">
			{srcJob.role}
		</h1>
		<div class="mb-4 text-slate-600 before:">
			{#if !srcJob.remote}
				Remote |
			{/if}
			{srcJob.location}
		</div>
		<div>
			{srcJob.role_description}
		</div>
		<h2 class="text-xl font-semibold">Requirements</h2>
		<ul class="list-disc">
			{#each srcJob.requirements as requirement}
				<li>{requirement}</li>
			{/each}
		</ul>
		<h2 class="text-xl font-semibold">Opportunities</h2>
		<ul class="list-disc">
			{#each srcJob.key_points as key_point}
				<li>{key_point}</li>
			{/each}
		</ul>
		{#if !relatedApplication}
			<div class="flex justify-evenly mt-4">
				<button class="bg-red-400" on:click={reject}>Reject</button>
				<button class="bg-green-400" on:click={apply}>Apply</button>
			</div>
		{/if}
		<div />
	</div>
	{#if relatedApplication?.application_processed}
		<JobApplicationForm {srcJob} srcApplication={relatedApplication} />
	{/if}
</div>
{/if}


<style type="postcss">
	#card {
		@apply bg-white max-w-2xl my-4 p-12 rounded-xl shadow-md relative z-10;
	}

	h1 {
		@apply text-2xl font-medium;
	}

	#banner {
		@apply  text-white text-center p-1 absolute top-0 left-0 right-0 rounded-t-xl;
	}
</style>
