<script>
	import { login } from '$lib/requestUtils.ts'

	let email, password

	function loginClickHandler() {
		login(email, password)
	}
	
</script>


<div class="form">
	<label for="nameInput">
		Email
		<input bind:value={email}><br>
	</label>
	<label for="nameInput">
		Password
		<input bind:value={password}><br>
	</label>

	<div on:click={loginClickHandler}>Login</div>
</div>