<script lang="ts">
    export let data
    import Icon from '@iconify/svelte';
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
    <div class="bg-white p-6 m-4 flex items-center gap-4 shadow-md rounded-xl">
        <h2>Active Jobs Processed/Scraped</h2>
        <p class="metric">{metrics.processedJobsCount}/{metrics.activeJobsCount}</p>
    </div>
    
    <div class="bg-white p-6 m-4 items-center gap-4 shadow-md rounded-xl">
        <h2>Users ({metrics.userCount})</h2>
        <div class="">
            {#each users as user}
            <div class="mt-2 p-2 rounded-lg text-white bg-orange-400 flex">
                <div>
                    <div class="">{user.name}</div>
                    <div class="text-sm">{user.email}</div>    
                </div>
                <div class="ml-auto w-10">
                    {#if user.permission == "admin"}
                        <Icon class="h-full w-full" icon="solar:shield-user-bold"/>
                    {:else if user.permission == "candidate"}
                        <Icon class="h-full w-full" icon="solar:user-check-rounded-bold"/>
                    {:else if user.permission == "unverified"}
                        <Icon class="h-full w-full" icon="solar:user-rounded-bold"/>
                    {/if}
                </div>
            </div>
            {/each}
        </div>
    </div>
</div>

<style type="postcss">
    h2 {
        @apply text-2xl font-semibold;
    }

    p.metric {
        @apply text-4xl;
    }
</style>