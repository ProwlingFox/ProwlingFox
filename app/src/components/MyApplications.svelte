<script lang="ts">
	import { applications as as } from '$lib/myJobs'
	import Icon from '@iconify/svelte'
	import {
		type Application,
		ApplicationStatus,
		applicationStatusLookup
	} from '$interfaces/application'

	const { receive } = $as

</script>

<div id="container" class="flex w-full flex-grow md:w-auto md:flex-grow-0 min-w-[20rem]">
	<div
		class="text-center p-2 text-xl font-medium text-white bg-amber-800">
		Current Applications
	</div>
	<ul class="overflow-y-auto overflow-x-hidden flex-grow p-0">
		{#if !$as.applications.length}
			<div class="text-white text-xl h-full flex flex-col justify-center items-center">
				<div class="flex flex-col items-center font-light pb-20">
					<Icon height="6em" inline={false} icon="ion:file-tray"/>
					No Applications In Progress
				</div>
			</div>
		{/if}
		{#each $as.applications as app (app._id)}
			{@const progress = applicationStatusLookup[app.status]}
			<a href={"/jobs/" + app.job_id}>
				<li in:receive={{ key: app._id }}>
					<div class="text-lg font-bold">{app.job.company.name}</div>
					<div class="text-sm font-light">{app.job.role}</div>
					<div class="flex items-center">
						<div class="h-3 w-3/5 border-2 rounded-full">
							<div
								class="{progress.color} h-full rounded-full"
								style="width: {progress.percent}%" />
							</div>
						<div class="text-sm w-2/5 ml-1">
							{progress.shortLabel}
						</div>
					</div>
				</li>
			</a>
		{/each}
	</ul>
</div>

<style type="postcss">
	#container {
		@apply w-80 bg-[#cb642c] rounded-lg shadow-lg m-2 overflow-hidden flex-col;
	}

	li {
		@apply bg-white p-2 m-2 rounded-md shadow;
	}
</style>
