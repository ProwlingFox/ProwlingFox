<script lang="ts">
	export let carouselMove: Function
	import Button from '$components/common/Button.svelte'

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
				<Button color="orange" label="Back" on:click={carouselBack} />
				<Button color="orange" label="Next" on:click={carouselNext} />
			</div>
		</div>
	</div>
</div>
