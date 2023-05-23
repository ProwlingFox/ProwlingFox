<script lang="ts">
    export let data
    import Icon from '@iconify/svelte';
	import type { User } from '$interfaces/user'
    import { parseJWT } from '$lib/requestUtils'
    import Chart from 'chart.js/auto'
    import type { ChartOptions } from 'chart.js';


    interface OpenAIUsage {
        prompt_tokens: number,
        completion_tokens: number,
        total_tokens: number,
        count: number,
        date: Date,
        model: string,
        label: string
    }

    interface Metrics {
        activeJobsCount: number,
        processedJobsCount: number,
        userCount: number,
        jobApplicationCount: number,
        averageAIQuestionsPerJob: number,
        openAIUsage: OpenAIUsage[]
    }

    parseJWT()
    let jobInjestCost: HTMLCanvasElement | undefined
    let jobInjestCount: HTMLCanvasElement | undefined

    let metrics: Metrics = data.metrics
    let users: User[] = data.users

    let dateGroupedOpenAI: {
        [key:number]: {
            date: Date,
            openAiUsage: {[key:string]: OpenAIUsage}
        }
    } = {}
    // Group OpenAIUsage By Date
    data.metrics.openAIUsage.forEach((x: OpenAIUsage) => {
        x.date = new Date(x.date)

        if (x.date.getTime() in dateGroupedOpenAI) {
            dateGroupedOpenAI[x.date.getTime()].openAiUsage[x.label] = x
        } else {
            dateGroupedOpenAI[x.date.getTime()] = {
                date: x.date,
                openAiUsage: { [x.label] : x}
            }
        }
    })

    console.log(dateGroupedOpenAI)

    const options: ChartOptions<'line'> = {
        scales: {
            x: {
                type: 'linear',
            }
        },
        elements: {
            line: {
                tension: 0.3
            }
        }
    }

    $: if(jobInjestCount) {
        new Chart(jobInjestCount,
            {
                type: 'line',
                data: getDataFromOpenAIUsage('Count Of Jobs Injested', x => x.MatchRole?.count ?? 0),
                options: options
            }
        );
    }

    $: if(jobInjestCost) {
        new Chart(jobInjestCost,
            {
                type: 'line',
                // Currency Calc In $
                data: getDataFromOpenAIUsage('$ Per 1000 Jobs Injested', x => {
                    return (
                    (x.MatchRole?.total_tokens ?? 0)                * 0.0004 +
                    (x.multiPreprocess?.total_tokens ?? 0)          * 0.002 +
                    (x.summarizeJobDescription?.total_tokens ?? 0)  * 0.002 + 
                    (x.roleRequirements?.total_tokens ?? 0)         * 0.002 + 
                    (x.roleKeyPoints?.total_tokens ?? 0)            * 0.002 + 
                    (x.questionPreprocessor?.total_tokens ?? 0)     * 0.002
                    ) / x.multiPreprocess?.count
                }),
                options: options
            }
        );
    }
    
    function getDataFromOpenAIUsage(label: string, fn: (x: {[key:string]: OpenAIUsage}) => any) {
        return {
            labels: Object.keys(dateGroupedOpenAI).sort((a, b) => parseInt(b) - parseInt(a)),
            datasets: [
            {
                label: label,
                data: Object.values(dateGroupedOpenAI).sort((a, b) => b.date.getTime() - a.date.getTime()).map(x => x.openAiUsage).map(fn)
            }
            ]
        }
    }



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

    <div>
        <canvas bind:this={jobInjestCount}></canvas>
    </div>
    <div>
        <canvas bind:this={jobInjestCost}></canvas>
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