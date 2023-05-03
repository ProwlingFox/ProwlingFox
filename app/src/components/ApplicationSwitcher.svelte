<script lang="ts">
	import { afterNavigate, beforeNavigate } from "$app/navigation"
    import MyJobs from "$components/MyApplications.svelte"

    let innerWidth = 0
    export let selectedTab = "Main"
    const mainTabName = selectedTab;
    const WIDTH_CHANGE_PX = 768

    afterNavigate(() => {
        selectedTab = mainTabName
    })
</script>

<svelte:window bind:innerWidth />

<div class="flex flex-col w-full">
    <div class="flex flex-grow overflow-auto">
        {#if (innerWidth > WIDTH_CHANGE_PX) || (selectedTab == "Applications")}
            <MyJobs/>
        {/if}
        {#if (innerWidth > WIDTH_CHANGE_PX) || (selectedTab == mainTabName)}
            <slot/>
        {/if}
    </div>
    <div class="bg-orange-700 text-white z-30 flex md:hidden justify-around shadow-black shadow-xl">
        <button on:click={() => {selectedTab = mainTabName}} class="p-4 w-full">
            {mainTabName}
        </button>
        <button on:click={() => {selectedTab = "Applications"}} class="p-4 w-full">
            My Applications
        </button>
    </div>
</div>