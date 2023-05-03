<script lang="ts">
	import JobCard from '$components/JobCard.svelte'
	import type { Job } from '$interfaces/job'

	export let data
	let job: Job
	$: job = data.job
</script>

<div class="flex justify-center items-start">
	<JobCard srcJob={job}></JobCard>
</div>