<script lang="ts">
	import type { User } from '$interfaces/user'
	import FormContainer from './FormContainer.svelte'
	import { Input, Label } from 'flowbite-svelte'
	import MultiSelect from 'svelte-multiselect'
	// import MultiSelect from '../../../node_modules/svelte-multiselect'

	let options: string[] = []

	export let carouselMove: Function
	export let user: User
</script>

<FormContainer {carouselMove} back={true} submit={false}>
	<div class="p-2">
		<Label class="block space-y-2">
			<span>Sector</span>
			<Input
				label="Name"
				name="Name"
				required
				placeholder="IT"
				bind:value={user.job_preferences.sector} />
		</Label>
	</div>

	<div class="p-2">
		<Label class="block space-y-2">
			<span>Roles</span>
			<MultiSelect
				{options}
				highlightMatches={false}
				liSelectedClass="hidden"
				allowEmpty={true}
				placeholder="Fullstack Developer"
				createOptionMsg="Add role"
				allowUserOptions="append" />
		</Label>
	</div>
</FormContainer>

<style>
	:global(div.multiselect) {
		padding: 0 !important;
	}

	:global(div.multiselect button) {
		width: fit-content;
	}

	:global(div.multiselect > ul) {
		background-color: white !important;
		border-radius: 0.5rem !important;
	}

	:global(div.multiselect > ul > input) {
		padding: 0.625rem !important;
	}

	:global(div.multiselect > ul > input::placeholder) {
		padding: 0 !important;
		color: #666 !important;
	}

	:global(div.multiselect > svg) {
		display: none;
	}

	:global(div.multiselect > ul.options > span) {
		display: none !important;
	}
</style>
