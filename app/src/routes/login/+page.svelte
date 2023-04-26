<script lang="ts">
	import { login } from '$lib/requestUtils'
	import { invalidateAll } from '$app/navigation'

	let email: string, password: string

	async function loginClickHandler() {
		const loggedIn = await login(email, password)

		if (loggedIn) {
			invalidateAll()
		}
	}

	function handleEnterKey(e: KeyboardEvent): void {
		if (e.key === 'Enter') {
			loginClickHandler()
		}
	}
</script>

<div class="w-full ml-auto mr-auto">
	<div class="flex justify-center">
		<div class="md:w-1/2">
			<div class="mt-20 mb-20">
				<div class=" rounded-lg">
					<div
						class="border-b border-gray-200 p-3 flex justify-center font-bold">
						<h6>Sign in</h6>
					</div>
					<div class="card-body p-6">
						<div class="flex flex-col justify-center">
							<div class="w-full">
								<label for="username">Email Address</label>
								<input
									type="text"
									class="block w-full p-3 m-1 rounded-lg bg-slate-50"
									id="email"
									placeholder="name@example.com"
									bind:value={email}
									on:keyup|preventDefault={handleEnterKey} />
							</div>
							<div class="w-full">
								<label for="password">Password</label>
								<input
									id="password"
									type="password"
									class="block w-full p-3 m-1 rounded-lg bg-slate-50"
									name="password"
									placeholder="Password"
									bind:value={password}
									on:keyup|preventDefault={handleEnterKey} />
							</div>
							<div
								class="admin__button-group button-group d-flex pt-1 justify-content-md-start justify-content-center">
								<button
									on:click={loginClickHandler}
									class="bg-slate-200 hover:bg-slate-300 p-2 w-full rounded-lg"
									>Sign In</button>
							</div>
						</div>
					</div>
					<div class="bg-slate-200 p-5 mt-2 flex justify-center">
						<p class="mb-0">
							Don't have an account?
							<a href="signup" class="text-blue-400"> Sign up </a>
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
