<script lang="ts">
	import type { User } from '$interfaces/user'
	import FormContainer from './FormContainer.svelte'
	import { Input, Label } from 'flowbite-svelte'
	export let carouselMove: Function
	export let user: User
</script>

<FormContainer {carouselMove} back={false}>
	<div class="p-2">
		<Label class="block space-y-2">
			<span>Name</span>
			<Input
				label="Name"
				name="Name"
				required
				placeholder="John Smith"
				bind:value={user.name} />
		</Label>
	</div>
	<div class="p-2">
		<Label class="block space-y-2">
			<span>Phone Number</span>
			<Input
				label="Name"
				name="Name"
				required
				placeholder="(123)-456-6789"
				bind:value={user.tel} />
		</Label>
	</div>
	<div class="p-2">
		<Label class="block space-y-2">
			<span>Pronouns</span>
			<Input
				label="Name"
				name="Name"
				required
				placeholder="He/Him"
				bind:value={user.pronouns} />
		</Label>
	</div>
</FormContainer>
