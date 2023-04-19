<script>
	import { applications as as } from '$lib/myJobs'
    
    const { receive } = $as

</script>

<div class="w-1/5 h-100% bg-[#cb642c]">
    <div class="text-center p-4 text-xl font-medium text-white border-b-2 border-cyan-950">
        My Applications
    </div>
    <ul>
        {#each $as.applications as app (app.id)}
            <li in:receive="{{key: app.id}}">
                <div class="text-lg font-bold">{app.companyName}</div>
                <div class="text-sm font-light">{app.role}</div>
            </li>
        {/each}
    </ul>
</div>

<style type="postcss">
    li {
        @apply bg-white p-2 m-2 rounded-md shadow;
    }
</style>