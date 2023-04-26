<script lang="ts">
    import JobCard from "$components/JobCard.svelte";
	import MyJobs from "$components/MyJobs.svelte"
    import { popNextJobID } from '$lib/myJobs'

    let nextJobId = popNextJobID()
</script>

<MyJobs/>
<div class="flex flex-col w-full m-2">
    {#await nextJobId then jobid}
        <a href={"/jobs/" + jobid} class="card w-full">
            <h2 class="text-2xl font-semibold">32 Jobs are waiting for you.</h2>
        </a>
    {/await}
    
    <div>
        
    </div>
</div>

<style lang="postcss">
    .card {
        @apply bg-white rounded-xl shadow p-12;
    }
</style>