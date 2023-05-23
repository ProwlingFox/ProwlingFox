<script lang="ts">
	import ApplicationCard from "$components/common/ApplicationCard.svelte"
    import { ApplicationStatus, type Application, applicationStatusLookup } from "$interfaces/application"
	import { Search } from "flowbite-svelte"

    export let sentApplications: Application[] = []

    let textFilter = ""

    let filter: {
        [key: string]: Boolean
    } = {
        Applied: true,
        Contacted: true,
        Interviewing: true,
        Offer: true,
    } 
    sentApplications[1].job.role
</script>

<div class="mt-2">
    <h3 class="text-xl font-semibold">Active Applications ({sentApplications.filter(x => x.status >= ApplicationStatus.Sent).length})</h3>
    <div class="flex gap-1">
        {#each Object.entries(filter) as [Key, Value]}
            <button 
                class={Value ? "selected" : ""}
                on:click={() => {filter[Key] = !Value}}
            >
                {Key}
            </button>
        {/each}
    </div>
    <Search size="md" class="my-2" bind:value={textFilter} />
    <div class="overflow-x-scroll">
        <div class="flex w-fit">
            {#each sentApplications as application}
                {#if application.job.role.toLowerCase().includes(textFilter.toLowerCase()) || application.job.company.name.toLowerCase().includes(textFilter.toLowerCase()) }
                    {#if filter.Applied && (application.status == ApplicationStatus.Sent)}
                        <ApplicationCard {application}/>
                    {:else if filter.Contacted && application.status == ApplicationStatus.Contact}
                        <ApplicationCard {application}/>
                    {:else if filter.Interviewing && application.status == ApplicationStatus.Interviewing}
                        <ApplicationCard {application}/>
                    {:else if filter.Offer && application.status >= ApplicationStatus.Offered}
                        <ApplicationCard {application}/>
                    {/if}
                {/if}
            {/each}
        </div>
    </div>
</div>

<style type="postcss">
    button.selected {
        @apply bg-orange-400 border-orange-600 border-solid border-2;
    }

    button {
        @apply text-sm font-semibold text-white px-2 bg-slate-400 border-slate-600 border-dashed border-2 rounded-xl;
    }
</style>