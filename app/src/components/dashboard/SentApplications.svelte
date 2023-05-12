<script lang="ts">
	import type { Application } from "$interfaces/application"

    export let sentApplications: Application[] = []
</script>

<div class="mt-2">
    <h3 class="text-xl font-semibold">Sent Applications ({sentApplications.filter(x => x.application_sent).length})</h3>
    <div class="overflow-x-scroll">
        <div class="flex w-fit">
            {#each sentApplications as application}
                {#if application.application_sent}
                    <a href={"/jobs/" + application.job_id} class="bg-white p-4 my-2 mr-4 w-80 h-52 shadow rounded-xl">
                        <div class="text-xl">{application.job.role}</div>
                        <div class="font-light">{application.job.company.name}</div>
                    </a>
                {/if}
            {/each}
        </div>
    </div>
</div>