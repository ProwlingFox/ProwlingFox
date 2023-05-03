<script lang="ts">
	import Overview from "$components/profileTabs/Overview.svelte";
	import SearchPreferences from "$components/profileTabs/SearchPreferences.svelte";
	import DataCollection from "$components/profileTabs/DataCollection.svelte";
	import Settings from "$components/profileTabs/Settings.svelte";

	export let data;
	let userInfo = data.userInfo
	let selection = "Role Preferences"

	const categories = [
		// "Overview",
		"Role Preferences",
		"Data Collection",
		"Settings"
	]

</script>

<div class="md:m-4 flex flex-col-reverse md:flex-row bg-white flex-grow shadow rounded-xl">
	<div class="shadow md:h-full w-full md:w-40 md:min-w-[10rem] rounded-xl">
		<div class="hidden md:block w-full p-4 text-center font-bold text-lg border-b-2">
			My Profile
		</div>
		<ul class="flex md:flex-col">
			{#each categories as category}
				<button 
					on:click={() => {selection = category}}
					class="w-full p-4 hover:bg-amber-200 {category == selection ? "bg-amber-300" : ""}"
				>
					{category}
				</button>
			{/each}
		</ul>
	</div>
	<div class="flex flex-col flex-grow overflow-auto">
		<Overview {userInfo}/>
		{#if selection == "Role Preferences"}
		<SearchPreferences {userInfo}/>
		{:else if selection == "Data Collection"}
		<DataCollection {userInfo}/>
		{:else if selection == "Settings"}
		<Settings {userInfo}/>
		{/if}
	</div>
</div>