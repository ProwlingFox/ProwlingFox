<script>
	import JobCard from '$components/job/JobCard.svelte'
	import type { Job } from '$interfaces/job'

	export let data
	let job: Job
	$: job = data.job
</script>

<div class="flex justify-center">
	<JobCard srcJob={job}></JobCard>
</div>