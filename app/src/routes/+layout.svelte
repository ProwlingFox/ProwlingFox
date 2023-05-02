<script lang="ts">
	import '../app.postcss'
	import { parseJWT } from '$lib/requestUtils'
	import {Avatar, Dropdown, DropdownHeader, DropdownItem, DropdownDivider} from 'flowbite-svelte'
	import { goto } from '$app/navigation'

	export let data


	let JWT = parseJWT()
	let authenticated = false

	$: {
		authenticated = data.authenticated
		JWT = parseJWT()
	}


	function signOut() {
		document.cookie = "token=;expires=Thu, 01 Jan 1970 00:00:00 GMT"
		goto("/login")
	}
</script>

<nav>
	<a href="/">
		<header>
			<h1>ProwlingFox</h1>
			<h2>Helping you catch the career you're looking for.</h2>
		</header>
	</a>
	{#if JWT && authenticated && ["admin", "candidate"].includes(JWT.permission)}
	<div class="mr-4 ml-auto self-center z-50">
		<Avatar id="user-drop" src={JWT?.profileImage ?? "/default-avatar.jpg"}/>
		<Dropdown  triggeredBy="#user-drop">
			<DropdownHeader>
			<span class="block text-sm"> {JWT.name} </span>
			<span class="block truncate text-sm font-medium"> {JWT.email} </span>
			</DropdownHeader>
			<DropdownItem href="/">Dashboard</DropdownItem>
			<DropdownItem href="/profile">Profile</DropdownItem>
			{#if JWT.permission == "admin"}
			<DropdownItem href="/admin">Admin</DropdownItem>
			{/if}
			<DropdownDivider />
			<DropdownItem on:click={signOut}>Sign out</DropdownItem>
		</Dropdown>
	</div>
	{/if}
</nav>

<main class="flex flex-grow">
	<slot />
</main>

<style type="postcss">
	main {
		@apply overflow-hidden;
	}

	nav {
		@apply bg-orange-800 text-white flex;
	}

	header {
		@apply m-2 ml-4;
	}

	h1 {
		@apply leading-none m-0 mb-0.5;
		font-family: 'Fredoka', sans-serif;
		font-weight: 300;
		font-size: 2rem;
	}

	h2 {
		@apply leading-none m-0;
		font-family: 'Fredoka', sans-serif;
		font-size: 0.825rem;
		font-weight: 400;
	}
</style>
