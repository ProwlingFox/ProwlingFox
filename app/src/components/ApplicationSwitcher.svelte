<script lang="ts">
	import { afterNavigate, beforeNavigate, goto } from "$app/navigation"
    import MyJobs from "$components/MyApplications.svelte"
	import Icon from "@iconify/svelte"

    let innerWidth = 0
    export let homePage = false
    let selectedTab = "Main"
    const mainTabName = selectedTab;
    const WIDTH_CHANGE_PX = 768

    afterNavigate(() => {
        selectedTab = mainTabName
    })
</script>

<svelte:window bind:innerWidth />

<div class="flex flex-col w-full">
    <div class="flex flex-grow overflow-hidden overflow-y-auto">
        {#if (innerWidth > WIDTH_CHANGE_PX) || (selectedTab == "Applications")}
            <MyJobs/>
        {/if}
        {#if (innerWidth > WIDTH_CHANGE_PX) || (selectedTab == mainTabName)}
            <slot/>
        {/if}
    </div>
    <div class="bg-orange-700 text-white z-30 flex md:hidden justify-around shadow-black shadow-xl">
        {#if !homePage}
            <button on:click={() => {selectedTab = "Main"}} class="p-1 w-full text-center {selectedTab == "Main" ? "selected" : ""}">
                <Icon class="w-full h-7" icon="material-symbols:work"/>
                <div class="text-xs leading-4">Current Role</div>
            </button>
        {/if}
        <button on:click={() => {if (!homePage) {goto("/")} else {selectedTab = "Main"}}} class="p-1 w-full text-center {selectedTab == "Main" && homePage ? "selected" : ""}">
            <Icon class="w-full h-7" icon="iconamoon:home-bold"/>
            <div class="text-xs leading-4">Home</div>
        </button>
        <button on:click={() => {selectedTab = "Applications"}} class="p-2 w-full text-center {selectedTab == "Applications" ? "selected" : ""}">
            <Icon class="w-full h-7" icon="icon-park-solid:inbox"/>
            <div class="text-xs leading-4">Applications</div>
        </button>
    </div>
</div>

<style lang="postcss">
    button.selected {
        @apply bg-orange-800;
    }
</style>