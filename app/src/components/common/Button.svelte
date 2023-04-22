<script lang="ts">
	export let color: string
	export let label: string

	interface ColorVariants {
		[key: string]: string
		orange: string
	}

	let colorVariants: ColorVariants = {
		orange: 'text-white bg-orange-700 hover:bg-orange-600 focus:ring-orange-300',
	}
</script>

<button
	on:click
	class="{colorVariants[
		color
	]} text-center font-medium focus:ring-4 focus:outline-none inline-flex items-center justify-center px-5 py-2.5 text-sm rounded-lg">
	{label}
</button>
