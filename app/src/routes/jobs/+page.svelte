<script>
	import { get } from '$lib/requestUtils.ts'
	import { onMount } from 'svelte'

	let jobs = '';
	let test;

	onMount(() => {
		get('http://localhost:8000/jobs').then((res) => {
			jobs = res.data
			console.log(jobs)
		})
	})
	
</script>

<div id="JobBoard">
	{#each jobs as job}
		<div class="jobListing">
			<div class="jobTitle">{job.jobTitle}</div>
			<div class="jobCompany">{job.company}</div>
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