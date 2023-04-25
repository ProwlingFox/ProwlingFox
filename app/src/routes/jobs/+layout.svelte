<script lang="ts">
    import MyJobs from '$components/MyJobs.svelte'
	import { isJWTValid } from '$lib/requestUtils'
</script>

{#if isJWTValid()}
    <MyJobs></MyJobs>
{/if}
<div class="flex-grow h-full overflow-auto p-0">
    <slot />
</div>