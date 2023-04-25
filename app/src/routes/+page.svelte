<script lang="ts">
    import JobCard from "$components/JobCard.svelte";
	import MyJobs from "$components/MyJobs.svelte"
</script>

<MyJobs/>
<div class="card">
    32 Jobs are waiting for you
</div>

<style lang="postcss">
    .card {
        @apply bg-white rounded-xl shadow
    }
</style>