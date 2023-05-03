<script lang="ts">
    import ApplicationSwitcher from "$components/ApplicationSwitcher.svelte"
    import { popNextJobID, userJobsLeft } from '$lib/myJobs'    

    let nextJobId = popNextJobID()
</script>

<ApplicationSwitcher mainTabName="Home">
    <div class="flex flex-col w-full m-2">
        {#await nextJobId then jobid}
            <a href={"/jobs/" + jobid} class="bg-white rounded-xl shadow p-12 card w-full">
                <h2 class="text-2xl font-semibold">{$userJobsLeft} opportunities are waiting for you.</h2>
            </a>
        {/await}
    </div>
</ApplicationSwitcher>