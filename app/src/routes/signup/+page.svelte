<script>
	import { login } from '$lib/requestUtils'

	interface User {
		name: string
		email: string
		pass: string
		passConfirm: string
	}

	let user: User = {
		name: '',
		email: '',
		pass: '',
		passConfirm: '',
	}

	function validatePassword(pass: string, confirmationPass: string) {
		if (pass != confirmationPass) {
			return false
		}

		return true
	}

	function validateEmail(email: string) {
		return true
	}

	async function createAccount() {
		if (!validatePassword(user.pass, user.passConfirm)) {
			alert('invalidPassword')
			return
		}

		const body = {
			name: user.name,
			email: user.email,
			password: user.pass,
		}

		const response = await fetch('/user/create', {
			method: 'POST',
			body: JSON.stringify(body),
			headers: {
				'content-type': 'application/json',
			},
		})

		if (response.ok) {
			login(user.email, user.pass)
		} else {
			alert('Signup Error')
		}
	}

	function handleEnterKey(e: KeyboardEvent): void {
		if (e.key === 'Enter') {
			createAccount()
		}
	}
</script>

<div class="w-full ml-auto mr-auto">
	<div class="flex justify-center">
		<div class="md:w-1/2">
			<div class="mt-20 mb-20">
				<div class="bg-white rounded-lg">
					<div
						class="border-b border-gray-200 p-3 flex justify-center font-bold">
						<h6>Sign Up</h6>
					</div>
					<div class="card-body p-6">
						<div class="flex flex-col justify-center">
							<div class="w-full">
								<label for="username">Name</label>
								<input
									type="text"
									class="block w-full p-3 m-1 rounded-lg bg-slate-200"
									id="name"
									placeholder="John Doe"
									bind:value={user.name}
									on:keyup|preventDefault={handleEnterKey} />
							</div>
							<div class="w-full">
								<label for="username">Email Address</label>
								<input
									type="text"
									class="block w-full p-3 m-1 rounded-lg bg-slate-200"
									id="email"
									placeholder="name@example.com"
									bind:value={user.email}
									on:keyup|preventDefault={handleEnterKey} />
							</div>
							<div class="w-full">
								<label for="password">Password</label>
								<input
									id="password"
									type="password"
									class="block w-full p-3 m-1 rounded-lg bg-slate-200"
									name="password"
									placeholder="Password"
									bind:value={user.pass}
									on:keyup|preventDefault={handleEnterKey} />
							</div>
							<div class="w-full">
								<label for="password">Confirm Password</label>
								<input
									id="password-confirm"
									type="password"
									class="block w-full p-3 m-1 rounded-lg bg-slate-200"
									name="password-confirm"
									placeholder="Password"
									bind:value={user.passConfirm}
									on:keyup|preventDefault={handleEnterKey} />
							</div>
							<div
								class="admin__button-group button-group d-flex pt-1 justify-content-md-start justify-content-center mt-5">
								<button
									on:click={createAccount}
									class="bg-slate-300 hover:bg-slate-400 p-2 w-full rounded-lg"
									>Create Account</button>
							</div>
						</div>
					</div>
					<!-- End: .card-body -->
				</div>
			</div>
		</div>
	</div>
</div>
