<script>
	import '../app.postcss'
	import { parseJWT } from '$lib/requestUtils'
	import MyJobs from '$components/MyJobs.svelte'

	export let data
	
	const JWT = parseJWT()
	const role = JWT?.permission
</script>

<nav>
	<header>
		<h1>Job.Ai</h1>
		<h2>Lorem Ispum Dolor Sat Amen</h2>
	</header>
	{#if data.authenticated}
		<ul>
			<a href="/jobs">Jobs</a>
			<a href="/profile">Profile</a>
			{#if role == "admin"}
				<a href="/admin">Admin</a>
			{/if}
		</ul>
	{/if}
</nav>

<main class="flex flex-grow">
	{#if data.authenticated}
		<MyJobs></MyJobs>
	{/if}
	<div class="flex-grow h-full overflow-hidden">
		<slot />
	</div>
</main>

<style type="postcss">
	@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@300&family=Nunito&display=swap');
	@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,500;1,600;1,700;1,800&display=swap');

	:global(:root) {
		font-family: 'Inter', sans-serif;
	}

	:global(body) {
		margin: 0px;
	}

	main {
		@apply overflow-hidden;
	}

	nav {
		@apply bg-cyan-900 text-white;
		display: flex;
		flex-direction: row;
	}

	header {
		margin: 0.25em 1em;
	}

	h1 {
		font-family: 'IBM Plex Sans Condensed', sans-serif;
		font-weight: 300;
		font-size: 2rem;
		margin: 0px;
	}

	h2 {
		font-size: 0.75rem;
		font-weight: 400;
		margin: 0px;
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
		padding: 1.2em 1em;
		text-decoration: none;
		color: inherit;
	}

	ul > a:hover {
		background-color: rgba(0, 0, 0, 0.15);
	}
</style>
