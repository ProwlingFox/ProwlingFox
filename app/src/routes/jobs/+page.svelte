<script>
	import { get } from '$lib/requestUtils'
	import { onMount } from 'svelte'
	import type { Job } from '$interfaces/job'

	import type { PageData } from './$types';
	export let data: PageData

	let jobs: Job[] = data.jobs
</script>

<div id="JobBoard" class="h-full overflow-auto">
	{#each jobs as Job}
		<a href="/jobs/{Job.id}" >
			<div class="jobListing">
				<div class="jobTitle">{Job.role}</div>
				<div class="jobCompany">{Job.company.name}</div>	
			</div>
		</a>
	{/each}
</div>

<style>


	.jobListing {
		margin: 1em;
		padding: 1em;
		border: 1px solid black;
	}

	.jobTitle {
		font-size: 1.5em;
	}
</style>
