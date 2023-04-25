<script lang="ts">
	import '../app.postcss'
	import { parseJWT } from '$lib/requestUtils'

	export let data
	
	const JWT = parseJWT()
	const role = JWT?.permission
</script>

<nav>
	<a href="/">
		<header>
			<h1>ProwlingFox</h1>
			<h2>Helping you catch the career you're looking for.</h2>
		</header>
	</a>
	{#if data.authenticated}
		<ul>
			<a href="/jobs"><p>Jobs</p></a>
			<a href="/profile"><p>Profile</p></a>
			{#if role == "admin"}
				<a href="/admin"><p>Admin</p></a>
			{/if}
		</ul>
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

	ul {
		margin: 0px;
		margin-left: auto;
		display: flex;
		flex-direction: row;
		list-style-type: none;
		align-items: center;
		font-size: 1.125em;
	}

	ul > a {
		@apply h-full flex items-center px-2;
		text-decoration: none;
		color: inherit;
	}

	ul > a:hover {
		background-color: rgba(0, 0, 0, 0.15);
	}
</style>
