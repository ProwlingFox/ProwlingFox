<script>
	import { login } from '$lib/requestUtils'
	import { goto } from '$app/navigation';

	let email: string, password: string

	async function loginClickHandler() {
		const loggedIn = await login(email, password)
		console.log('loggedIn', loggedIn)
		if (loggedIn) {
			goto('/jobs')
		}
	}

	function handleEnterKey(e: KeyboardEvent<HTMLInputElement>): void {
    if (e.key === "Enter") {
      loginClickHandler();
    }
  }

</script>


<div class="w-full ml-auto mr-auto">
	<div class="flex justify-center">
	   	<div class="md:w-1/2">
			<div class="mt-20 mb-20 ">
				<div class="flex justify-center mb-6">
					<a href="index.html" class="bg-white w-fit p-4 rounded-2xl">
						<h1 class="font-bold inline">Job.Ai</h1>
					</a>
				</div>
				<div class="bg-white rounded-lg">
					<div class="border-b border-gray-200 p-3 flex justify-center font-bold">
						<h6>Sign in</h6>
					</div>
					<div class="card-body p-6">
						<div class="flex flex-col justify-center">
							<div class="w-full">
								<label for="username">Email Address</label>
								<input type="text" class="block w-full p-3 m-1 rounded-lg bg-slate-200" id="email" placeholder="name@example.com" bind:value={email} on:keyup|preventDefault={handleEnterKey}>
							</div>
							<div class="w-full">
								<label for="password-field">Password</label>
								<!-- <div class="position-relative "> -->
									<input id="password-field" type="password" class="block w-full p-3 m-1 rounded-lg bg-slate-200" name="password" placeholder="Password" bind:value={password} on:keyup|preventDefault={handleEnterKey}>
									<!-- <div class="uil uil-eye-slash text-lighten fs-15 field-icon toggle-password2">
									</div> -->
								<!-- </div> -->
							</div>
							<div class="flex items-center justify-between mt-5 mb-5">
								<div class="checkbox">
									<input class="checkbox" type="checkbox" id="check-1">
									<label for="check-1">
									<span class="checkbox-text">Keep me logged in</span>
									</label>
								</div>
								<a href="forget-password.html">Forgot password?</a>
							</div>
							<div class="admin__button-group button-group d-flex pt-1 justify-content-md-start justify-content-center">
								<button on:click={loginClickHandler} class="bg-slate-300 hover:bg-slate-400 p-2 w-full rounded-lg">Sign In</button>
							</div>
						</div>
					</div><!-- End: .card-body -->
				<!-- <div class="px-5">
					<p class="social-connector text-center
						before:bg-gray-200 before:h-[1px] before:inline-block before:w-1/3 before:align-middle before:mr-3
						after:bg-gray-200 after:h-[1px] after:inline-block after:w-1/3 after:align-middle after:ml-3
					">
						<span>Or</span>
					</p>
					<div class="flex justify-center">
						<img class="h-14 hover:cursor-pointer" src="/btn_google_signin_light_normal_web@2x.png" alt="">
					</div>
				</div> -->
				<div class="bg-slate-200 p-5 mt-2 flex justify-center">
				   <p class="mb-0">
					  Don't have an account?
					  <a href="sign-up.html" class="text-blue-400">
						 Sign up
					  </a>
				   </p>
				</div>
			</div>
		  </div>
	   </div>
	</div>
 </div>
