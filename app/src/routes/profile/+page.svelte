<script>
	import { parseJWT, post } from '$lib/requestUtils'

	// console.log(parseJWT())

	async function setUserData() {
		const body = {
			name: 'Liaaaaaa',
			tel: '123-456-7890',
			pronouns: 'she/her',
			job_preferences: {
				roles: ['Frontend', 'Backend'],
				sector: 'IT',
				locations: ['New York, New York'],
				remote: true,
				salary: 100000,
			},
		}

		const response = await post('/user/update', body)
		if (response.success) {
			console.log('hi')
		}
	}

	setUserData()
</script>

<div class="form">
	<label for="nameInput">
		Name
		<input /><br />
	</label>
</div>
