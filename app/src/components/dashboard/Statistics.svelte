<script lang="ts">
	import type { UserStats } from "$interfaces/user"

    export let statistics: UserStats
</script>

<div class="mt-4 w-100 flex gap-4 w-full">
    <!-- <div class="card w-1/4">

    </div> -->
    <div class="card flex-grow flex items-center justify-center">
        <span class="mr-2 font-bold">Applications Sent Today:</span>
        <strong class="font-light text-xl">{statistics.applicationsToday}</strong>
    </div>
    <!-- <div class="card w-1/4">

    </div> -->
</div>

<style class="postcss">
    .card {
        @apply bg-white shadow p-4 rounded-xl;
    }
</style>