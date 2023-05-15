<script lang="ts">
    export let data
	import type { User } from '$interfaces/user'
    import { parseJWT } from '$lib/requestUtils'


    interface Metrics {
        activeJobsCount: number,
        processedJobsCount: number,
        userCount: number,
        jobApplicationCount: number,
    }

    parseJWT()
    let metrics: Metrics = data.metrics
    let users: User[] = data.users
</script>

<div>
    <div class="card">
        <h2>Active Jobs Processed/Scraped</h2>
        <p class="metric">{metrics.processedJobsCount}/{metrics.activeJobsCount}</p>
    </div>
    
    <div class="card">
        <h2>Users ({metrics.userCount})</h2>
        <div>
            {#each users as user}
            <div>
                {user.name}
                {user.email}
            </div>
            {/each}
        </div>
    </div>
</div>

<style type="postcss">

    .card {
        @apply bg-white p-8 m-4 flex items-center gap-4 shadow-md;
        border-radius: 1em;
    }

    h2 {
        @apply text-2xl font-semibold;
    }

    p.metric {
        @apply text-4xl;
    }
</style>