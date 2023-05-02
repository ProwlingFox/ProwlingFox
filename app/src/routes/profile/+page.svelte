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

<div class="m-4 flex bg-white flex-grow shadow rounded-xl">
	<div class="shadow h-full w-40 min-w-[10rem] rounded-xl">
		<div class="w-full p-4 text-center font-bold text-lg border-b-2">
			My Profile
		</div>
		<ul>
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
	<div class="flex flex-col flex-grow">
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