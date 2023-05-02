<script lang="ts">
	import { login, loginLinkedIn } from '$lib/requestUtils'
	import { invalidateAll } from '$app/navigation'
	import { browser } from '$app/environment'
	import { PUBLIC_APP_URL, PUBLIC_LINKEDIN_CLIENT_ID } from '$env/static/public';

	export let data

	let email: string, password: string
	let loggedIn: boolean | null;

	if (data.code && browser) {
		loginLinkedIn(data.code).then(
			(success) => {
				loggedIn = success
				if (loggedIn) {
					invalidateAll()
				}
			}
		)
	}

	async function loginClickHandler() {
		loggedIn = await login(email, password)
		if (loggedIn) {
			invalidateAll()
		}
	}

	function handleEnterKey(e: KeyboardEvent): void {
		if (e.key === 'Enter') {
			loginClickHandler()
		}
	}

	function getLinkedInOAuthURI() {
		const url = new URL("https://www.linkedin.com/oauth/v2/authorization")
		const oauthParams: {[key: string]: string} = {
			response_type: "code",
			client_id: PUBLIC_LINKEDIN_CLIENT_ID,
			redirect_uri: PUBLIC_APP_URL + "/login",
			state: "",
			scope: "openid profile email"
		}

		Object.keys(oauthParams).forEach(key => url.searchParams.append(key, oauthParams[key]));
		return url.href
	}
</script>

<div class="flex justify-center w-full">
	<div class="flex flex-col items-center mt-16 max-w-lg w-full m-4 md:w-1/2">
		<img class="relative w-3/5 max-w-xs" src="/favicon.png" alt="ProwlingFox Logo"/>
		<div class="w-full pt-6 relative">
			{#if loggedIn === false}
				<div class="text-orange-700 text-center text-lg font-bold absolute top-0 w-full" >Incorrect Username or Password</div>
			{/if}
			<div class="w-full">
				<label class="font-semibold text-lg" for="username">Email Address</label>
				<input
					type="text"
					class="block bg-white w-full p-3 m-1 rounded-xl"
					id="email"
					placeholder="name@example.com"
					bind:value={email}
					on:keyup|preventDefault={handleEnterKey} />
			</div>
			<div class="w-full mt-2">
				<label class="font-semibold text-lg" for="password">Password</label>
				<input
					id="password"
					type="password"
					class="block bg-white w-full p-3 m-1 rounded-xl"
					name="password"
					placeholder="Password"
					bind:value={password}
					on:keyup|preventDefault={handleEnterKey} />
			</div>
			<div class="d-flex pt-1 justify-content-md-start justify-content-center">
				<button on:click={loginClickHandler} class=" bg-orange-400 hover:bg-orange-500 w-full">Sign In</button>
			</div>
			<div class="d-flex pt-1 justify-content-md-start justify-content-center mt-6">
				<a href={getLinkedInOAuthURI()} class="block text-center bg-teal-800 hover:bg-teal-500 w-full p-2 rounded-xl drop-shadow text-white">Sign In With LinkedIn</a>
			</div>
		</div>
		<!-- <p class="mb-0 mt-3">
			Don't have an account?
			<a href="signup" class="text-orange-700"> Sign up </a>
		</p> -->
	</div>
</div>

<style lang="postcss">
	button {
        @apply p-2 rounded-xl drop-shadow text-white;
    } 

	/* Change the white to any color */
	input:-webkit-autofill,
	input:-webkit-autofill:hover, 
	input:-webkit-autofill:focus, 
	input:-webkit-autofill:active{
		@apply bg-amber-50;
		-webkit-box-shadow: 0 0 0 30px rgb(254 236 220) inset !important;
	}

</style>