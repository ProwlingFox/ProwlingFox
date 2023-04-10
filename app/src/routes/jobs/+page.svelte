<script>
	import { get } from '$lib/requestUtils'
	import { onMount } from 'svelte'

	interface Job {
		'job_id': string
		'jobTitle': string
		'company': string
		'longListing': string
		'shortListing'?: string
	}

	let jobs: Job[] = []
	let test;

	onMount(() => {
		get('http://localhost:8000/jobs').then((res) => {
			jobs = res.data
			console.log(jobs)
		})
	})

</script>

<div id="JobBoard">
	{#each jobs as Job}
		<div class="jobListing">
			<div class="jobTitle">{Job.jobTitle}</div>
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