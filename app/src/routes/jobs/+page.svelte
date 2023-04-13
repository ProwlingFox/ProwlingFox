<script>
	import { get } from '$lib/requestUtils'
	import { onMount } from 'svelte'
	import type { Job } from '$interfaces/job'

	import type { PageData } from './$types';
	export let data: PageData

	let jobs: Job[] = data.jobs.data
	console.log(jobs)
</script>

<div id="JobBoard">
	{#each jobs as Job}
		<div class="jobListing">
			<a href="/job/{Job.job_id}" class="jobTitle">{Job.jobTitle}</a>
			<div class="jobCompany">{Job.company}</div>
		</div>
	{/each}
</div>

<style>
	#JobBoard {
	}

	.jobListing {
		margin: 1em;
		padding: 1em;
		border: 1px solid black;
	}

	.jobTitle {
		font-size: 1.5em;
	}

	.jobCompany {
	}
</style>
