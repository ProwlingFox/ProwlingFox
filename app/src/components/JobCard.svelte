<script lang="ts">
	import { goto } from '$app/navigation'
	import { ApplicationStatus, applicationStatusLookup, type Application as JobApplication } from '$interfaces/application'
	import type { Job } from '$interfaces/job'
	import { getApplicationByJobID } from '$lib/applications'

	import { applications as as, popNextJobID, userJobsLeft } from '$lib/myJobs'
	import { get, post } from '$lib/requestUtils'
	import JobApplicationForm from './JobApplicationForm.svelte'

	export let srcJob: Job
	export let relatedApplication: JobApplication | undefined;

	const { send } = $as

	let nextId: string | null

	async function updateCheck() {
		// If The Application is not in a stable state, do an update
		await new Promise(r => setTimeout(r, 5000));
		if (!relatedApplication) {return}
		if (!(relatedApplication.status == ApplicationStatus.Processed || relatedApplication.status >= ApplicationStatus.Sent)) {
			console.log("Checking For Progress...")
			relatedApplication = await getApplicationByJobID(srcJob._id)
		}
		updateCheck()
	}

	updateCheck()

	async function apply() {
		post(`/jobs/${srcJob._id}/mark`, { requestApply: true })
		as.update((a) => {
			return {
				applications: [
					{
						_id: srcJob._id,
						job_id: srcJob._id,
						job: srcJob,
						status: ApplicationStatus.Requested,
					},
					...a.applications,
				],
				send: $as.send,
				receive: $as.receive,
			}
		})
		loadNext()
	}

	async function loadNext() {
		nextId = await popNextJobID()
		await goto('/jobs/' + (await nextId))
		userJobsLeft.update(x => x-1)
	}

	function reject() {
		post(`/jobs/${srcJob._id}/mark`, { requestApply: false })
		//Discard Animation
		//Load New 2
		loadNext()
	}
</script>

{#key srcJob}
<div class="flex flex-col xl:flex-row w-full lg:w-auto">
	<div class="bg-white p-4 md:px-12 sm:rounded-xl xl:left-2 sm:mx-4 lg:mx-0 lg:max-w-2xl sm:my-4 md:py-8 shadow-md relative z-10" out:send={{ key: srcJob._id }}>
		{#if relatedApplication}
			<div id="banner" class="sm:rounded-t-xl {applicationStatusLookup[relatedApplication.status].color}">
				{applicationStatusLookup[relatedApplication.status].label}
			</div>
		{/if}
		<a href={srcJob.src_url} class="flex justify-center mt-6">
			<img src={srcJob.company.logo} alt="" />
		</a>

		<h1 class="mt-4">
			{srcJob.role}
		</h1>
		<div class="mb-4 text-slate-600 before:">
			{#if !srcJob.remote}
				Remote |
			{/if}
			{srcJob.location.city ? srcJob.location.city + ", " : ""} {srcJob.location.country}
		</div>
		<div>
			{srcJob.role_description}
		</div>
		<h2 class="text-xl font-semibold">Requirements</h2>
		<ul class="list-disc pl-4">
			{#key srcJob}
				{#each srcJob.requirements as requirement}
					<li>{requirement}</li>
				{/each}
			{/key}
		</ul>
		<h2 class="text-xl font-semibold">Opportunities</h2>
		<ul class="list-disc pl-4">
			{#key srcJob}
				{#each srcJob.key_points as key_point}
					<li>{key_point}</li>
				{/each}
			{/key}
		</ul>
			{#if !relatedApplication || relatedApplication.status < ApplicationStatus.Requested}
				<div class="z-50 fade md:shadow-black sticky bottom-2 w-full md:static md:shadow md:left-auto md:bottom-auto md:w-auto left-0 flex justify-center gap-8 mt-4 ">
					<button class="bg-red-500" on:click={reject}>Reject</button>
					<button class="bg-green-500" on:click={apply}>Apply</button>
				</div>
			{/if}
		<div />
	</div>
	{#if relatedApplication && relatedApplication.status >= ApplicationStatus.Processed}
		<JobApplicationForm {srcJob} srcApplication={relatedApplication} />
	{/if}
</div>
{/key}


<style type="postcss">
	h1 {
		@apply text-2xl font-medium;
	}

	.fade {
		box-shadow: 0px 0px 20px 20px white;
		background-color: rgba(255, 255, 255, 1)
	}

	button {
		@apply p-2 w-40 rounded-xl drop-shadow text-white;
	}

	#banner {
		@apply text-white text-center p-1 absolute top-0 left-0 right-0;
	}
</style>
