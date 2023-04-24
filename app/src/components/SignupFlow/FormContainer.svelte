<script lang="ts">
	import Button from '$components/common/Button.svelte'
	import { post } from '$lib/requestUtils'
	import type { User } from '$interfaces/user'

	export let carouselMove: Function
	export let back: boolean
	export let submit: boolean
	export let user: User | null = null

	async function setUserData(): Promise<void> {
		if (!user) return
		const response = await post('/user/update', user)
		if (response.success) {
			console.log('hi')
		}
	}

	function carouselNext() {
		carouselMove(true)
	}

	function carouselBack() {
		carouselMove(false)
	}
</script>

<div class="h-full w-[100vw] shrink-0">
	<div class="h-full w-full flex items-center justify-center">
		<div class="flex flex-col">
			<slot />
			<div class="flex justify-between">
				<Button
					color="orange"
					label="Back"
					on:click={carouselBack}
					classList={back ? '' : 'invisible'} />
				<Button
					color="orange"
					label={submit ? 'Submit' : 'Next'}
					on:click={submit ? setUserData : carouselNext} />
			</div>
		</div>
	</div>
</div>
