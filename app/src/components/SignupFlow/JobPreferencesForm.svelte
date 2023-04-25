<script lang="ts">
	import type { User } from '$interfaces/user'
	import FormContainer from './FormContainer.svelte'
	import { Input, Label, Helper } from 'flowbite-svelte'

	export let carouselMove: Function
	export let user: User
</script>

<FormContainer {carouselMove} back={true} submit={true} {user}>
	<Label class="block space-y-2">
		<span>Your email</span>
		<Input
			label="Name"
			name="Name"
			required
			placeholder="name@flowbite.com"
			bind:value={user.name} />
	</Label>
	<div class="m-2 flex flex-col">
		<label for="name" class="">Phone number</label>
		<input type="text" class="" bind:value={user.tel} />
	</div>
	<div class="m-2 flex flex-col">
		<label for="name" class="">Pronouns</label>
		<input type="text" class="" bind:value={user.pronouns} />
	</div>
</FormContainer>
