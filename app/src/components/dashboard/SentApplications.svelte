<script lang="ts">
	import ApplicationCard from "$components/common/ApplicationCard.svelte"
import { ApplicationStatus, type Application } from "$interfaces/application"

    export let sentApplications: Application[] = []
</script>

<div class="mt-2">
    <h3 class="text-xl font-semibold">Active Applications ({sentApplications.filter(x => x.status >= ApplicationStatus.Sent).length})</h3>
    <!-- <div>
        <button>Applied</button>
        <button>Contacted</button>
        <button>Interviewing</button>
        <button>Offer</button>
    </div> -->
    <div class="overflow-x-scroll">
        <div class="flex w-fit">
            {#each sentApplications as application}
                {#if application.status >= ApplicationStatus.Sent}
                    <ApplicationCard {application}/>
                {/if}
            {/each}
        </div>
    </div>
</div>