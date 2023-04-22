<script lang="ts">
	import { goto } from '$app/navigation'
	import type { Job } from '$interfaces/job'

	import { applications as as, popNextJobID, jobQueue } from '$lib/myJobs'
	import { get, post } from '$lib/requestUtils'
	import { get as getStore } from 'svelte/store'

	export let srcJob: Job

	const { send } = $as

	// let nextId: Promise<string>
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
		visible = false
		loadNext()
	}

	preLoadNext()
</script>

{#if visible}
	<div id="card" out:send={{ key: srcJob._id }}>
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
			{srcJob.short_description}
		</div>
		<div class="flex justify-evenly mt-4">
			<button class="bg-red-400" on:click={reject}>Reject</button>
			<button class="bg-green-400" on:click={apply}>Apply</button>
		</div>
		<div />
	</div>
{/if}

<style type="postcss">
	#card {
		@apply bg-white max-w-xl m-4 p-12 rounded-xl shadow-md;
	}

	h1 {
		@apply text-4xl font-medium;
	}

	button {
		@apply p-2 w-40 rounded-xl drop-shadow;
	}
</style>
