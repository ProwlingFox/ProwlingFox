<script lang="ts">
    import MyJobs from '$components/MyJobs.svelte'
	import { isJWTValid } from '$lib/requestUtils'
</script>

{#if isJWTValid()}
    <MyJobs></MyJobs>
{/if}
<div class="flex-grow h-full overflow-x-clip overflow-y-auto p-0">
    <slot />
</div>