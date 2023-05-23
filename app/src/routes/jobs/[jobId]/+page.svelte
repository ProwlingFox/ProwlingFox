<script lang="ts">
	import JobCard from '$components/JobCard.svelte'
	import OutOfListings from '$components/jobListing/OutOfListings.svelte';
	export let data
</script>

<div class="flex justify-center items-start">
	{#if data.job}
		<JobCard srcJob={data.job} relatedApplication={data.relatedApplication}></JobCard>
	{:else}
		<OutOfListings/>
	{/if}
</div>