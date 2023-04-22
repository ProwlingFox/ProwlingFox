<script lang="ts">
	import type { User } from '$interfaces/user'
	import FormContainer from './FormContainer.svelte'
	export let carouselNext: Function
	export let user: User
</script>

<FormContainer {carouselNext}>
	<div class="m-2 flex flex-col">
		<label for="name" class="">Name</label>
		<input type="text" class="" bind:value={user.name} />
	</div>
	<div class="m-2 flex flex-col">
		<label for="name" class="">Phone number</label>
		<input type="text" class="" bind:value={user.tel} />
	</div>
	<div class="m-2 flex flex-col">
		<label for="name" class="">Pronouns</label>
		<input type="text" class="" bind:value={user.pronouns} />
	</div>
</FormContainer>
