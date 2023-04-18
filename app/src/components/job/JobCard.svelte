<script>
	import { goto } from '$app/navigation'
    import type { Job } from '$interfaces/job'

    import { applications as as } from '$lib/myJobs'

    export let srcJob: Job

    const { send } = $as

    let visible = true

    function apply() {      
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

    function loadNext() {
        goto("/jobs/643849330f589f940289359b")
        visible = true
    }

    function reject() {
        //Send Read acknowlage to server
        //Discard Animation
        //Load New
    }

</script>

{#if visible}
    <div id="card" on:outroend="{loadNext}" out:send="{{key: srcJob.id}}">
        <div class="flex justify-center">
            <img src={srcJob.company.logo} alt="">
        </div>
        
        <h1 class="mt-4">
            {srcJob.role}
        </h1>
        <div class="mb-4 text-slate-600">
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