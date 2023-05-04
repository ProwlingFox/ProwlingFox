<script lang="ts">
    import { popNextJobID, userJobTags, userJobsLeft } from '$lib/myJobs'    
	import Icon from '@iconify/svelte'
</script>

{#await popNextJobID() then jobid}
    <a href={"/jobs/" + jobid} class="relative bg-gradient-to-tr from-orange-600 to-orange-400 rounded-xl shadow p-4 pl-6 pr-8 card w-full flex h-60">
        <h2 class="text-2xl font-black self-end w-3/4 text-orange-100"><strong class="block text-5xl font-extralight">{$userJobsLeft}</strong> Opportunities <br>are waiting for you.</h2>
        <div class="self-center ml-auto">
            <Icon class="w-20 h-20 mt-4 text-orange-100" icon="material-symbols:rocket-launch-rounded"/>
        </div>
        <ul id="tags" class="absolute flex flex-wrap text-sm gap-1 left-0 right-0 mx-4 max-h-24 overflow-hidden opacity-gradient">
            {#each $userJobTags as tag}
                <li class="bg-orange-400 p-0.5 px-1 rounded shadow-xl text-orange-100">{tag}</li>
            {/each}
        </ul>
    </a>
{/await}

<style lang="postcss">
    .opacity-gradient {
        -webkit-mask-image: radial-gradient(ellipse 150% 80% at 20% 10%, rgba(0,0,0,1) 0%, rgba(0,0,0,0));
    }
</style>