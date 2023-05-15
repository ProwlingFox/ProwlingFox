<script lang="ts">
    export let data
    import { parseJWT } from '$lib/requestUtils'


    interface Metrics {
        activeJobsCount: number,
        processedJobsCount: number,
        userCount: number,
        jobApplicationCount: number,
    }

    parseJWT()
    let metrics: Metrics = data.metrics
</script>

<div>
    <div class="card">
        <h2>Active Jobs Processed/Scraped</h2>
        <p class="metric">{metrics.processedJobsCount}/{metrics.activeJobsCount}</p>
    </div>
    
    <div class="card">
        <h2>Users</h2>
        <p class="metric">{metrics.userCount}</p>
    </div>
    
    <div class="card">
        <h2>Job Applications</h2>
        <p class="metric">{metrics.jobApplicationCount}</p>
    </div>
    
    <div class="card">
        <h2>Job Applications Per User Avg.</h2>
        <p class="metric">{metrics.jobApplicationCount / metrics.userCount}</p>
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