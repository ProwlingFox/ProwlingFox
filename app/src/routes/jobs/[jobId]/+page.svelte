<script lang="ts">
	import JobCard from '$components/JobCard.svelte'

	export let data
</script>

<div class="flex justify-center items-start">
	<JobCard srcJob={data.job} relatedApplication={data.relatedApplication}></JobCard>
</div>