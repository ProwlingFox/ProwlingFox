

<script>
	import { login } from '$lib/requestUtils.ts'

	let user = {
		name: null,
		email: null,
		pass: null,
		passConfirm: null
	}
	
	function validatePassword(pass, confirmationPass) {
		if (pass != confirmationPass) {
			return false
		}

		return true
	}

	function validateEmail(email) {
		return true
	}

	async function createAccount() {
		if (!validatePassword(user.pass, user.passConfirm)) {
			alert("invalidPassword")
			return
		}

		const body = {
			"name": user.name,
			"email": user.email,
			"password": user.pass
		}

		const response = await fetch('http://localhost:8000/user/create', {
			method: 'POST',
			body: JSON.stringify(body),
			headers: {
				'content-type': 'application/json'
			}
		})

		if(response.ok) {
			login(user.email, user.pass)
		} else {
			alert("Signup Error")
		}
	}
</script>


Create an account:

<div class="form">
	<label for="nameInput">
		Name
		<input bind:value={user.name}><br>
	</label>
	<label for="nameInput">
		Email
		<input bind:value={user.email}><br>
	</label>
	<label for="nameInput">
		Password
		<input bind:value={user.pass}><br>
	</label>
	<label for="nameInput">
		Confirm Password
		<input bind:value={user.passConfirm}><br>
	</label>

	<div on:click={createAccount}>Create Account</div>
</div>