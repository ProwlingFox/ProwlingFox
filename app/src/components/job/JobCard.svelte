<script>
	import { goto } from '$app/navigation'
    import type { Job } from '$interfaces/job'

    import { applications as as, popNextJobID, jobQueue } from '$lib/myJobs'
	import { get, post } from '$lib/requestUtils'
	import { get as getStore } from 'svelte/store'

    export let srcJob: Job

    const { send } = $as

    // let nextId: Promise<string>
    let nextId: string

    let visible = true
    post(`/jobs/${srcJob.id}/mark`, {"requestApply": false})

    async function apply() {    
        post(`/jobs/${srcJob.id}/mark`, {"requestApply": true})
        as.update((a) => {
            return {
                "applications": [
                    {
                        id: srcJob.id,
                        companyName: srcJob.company.name,
                        role : srcJob.role
                    },
                    ...a.applications
                ],
                "send": $as.send, 
                "receive": $as.receive
            }
        })
        visible = false
    }

    async function preLoadNext() {
        nextId = await popNextJobID()
        get("/jobs/" + nextId)
    }

    async function loadNext() {
        await goto("/jobs/" + await nextId)
        visible = true
        post(`/jobs/${srcJob.id}/mark`, {"requestApply": false})
        preLoadNext()
    }

    function reject() {
        //Discard Animation
        //Load New
        visible = false
    }

    preLoadNext()
</script>

{#if visible}
    <div id="card" on:outroend="{loadNext}" out:send="{{key: srcJob.id}}">
        <div class="flex justify-center">
            <img src={srcJob.company.logo} alt="">
        </div>
        
        <h1 class="mt-4">
            {srcJob.role}
        </h1>
        <div class="mb-4 text-slate-600 before:">
            {#if !srcJob.remote}
                Remote |
            {/if}
            {srcJob.location}
        </div>
        <div>
            {srcJob.short_description}
        </div>
        <div class="flex justify-evenly mt-4">
            <button class="bg-red-400" on:click={reject}>Reject</button>
            <button class="bg-green-400" on:click={apply}>Apply</button>
        </div>
        <div>

        </div>
    </div>
{/if}

<style type="postcss">

#card {
    @apply bg-white max-w-xl m-4 p-12 rounded-xl shadow-md;
}

h1 {
    @apply text-4xl font-medium;
}

button {
    @apply p-2 w-40 rounded-xl drop-shadow;
}

</style>