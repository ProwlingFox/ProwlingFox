<script lang="ts">
	import JobCard from '$components/JobCard.svelte'
	import type { Job } from '$interfaces/job'

	export let data
</script>

<div class="flex justify-center items-start">
	<JobCard srcJob={data.job} relatedApplication={data.relatedApplication}></JobCard>
</div>