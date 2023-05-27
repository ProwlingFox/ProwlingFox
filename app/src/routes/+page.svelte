<script lang="ts">
    import ApplicationSwitcher from "$components/ApplicationSwitcher.svelte"
	import CallToAction from "$components/dashboard/CallToAction.svelte"
	import SentApplications from "$components/dashboard/SentApplications.svelte"
	import Statistics from "$components/dashboard/Statistics.svelte"

	import type { Application } from "$interfaces/application"

    export let data
    let allApplications: Application[] = data.fullApplications
</script>

<ApplicationSwitcher homePage={true}>
    <div class="flex flex-col w-full m-2 overflow-x-hidden">
        <CallToAction/>
        <Statistics statistics={data.stats}/>
        <SentApplications sentApplications={allApplications}/>
    </div>
</ApplicationSwitcher>