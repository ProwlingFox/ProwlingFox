<script>
	export let carouselNext: Function
</script>

<div class="bg-orange-300 h-full w-[100vw] shrink-0">
	<div class="h-full w-full flex items-center justify-center">
		<div class="flex flex-col">
			<slot />
			<button
				on:click={carouselNext}
				class="ml-auto p-2 bg-orange-500 rounded">Next</button>
		</div>
	</div>
</div>
