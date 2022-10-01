<style>
	@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@300&family=Nunito&display=swap');

	:global(:root) {
		font-family: 'Nunito', sans-serif;
	}

	:global(body) {
		margin: 0px;
	}

	nav {
		background-color: #BBB;
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

<nav>
	<header>
		<h1>Job.Ai</h1>
		<h2>Lorem Ispum Dolor Sat Amen</h2>
	</header>
	<ul>
		<a href="/jobs">Jobs</a>
		<a href="/profile">Profile</a>
		<a href="/admin">Admin</a>
	</ul>
</nav>

<slot></slot>