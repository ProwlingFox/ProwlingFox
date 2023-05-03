<script lang="ts">
    import ApplicationSwitcher from "$components/ApplicationSwitcher.svelte"
	import CallToAction from "$components/dashboard/CallToAction.svelte"
    import { popNextJobID, userJobsLeft } from '$lib/myJobs'    

    let nextJobId = popNextJobID()
</script>

<ApplicationSwitcher selectedTab="Home">
    <div class="flex flex-col w-full m-2">
        <CallToAction/>
    </div>
</ApplicationSwitcher>