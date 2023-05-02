<script lang="ts">
	import { applications as as } from '$lib/myJobs'
	import Icon from '@iconify/svelte'
	import type {
		Application,
		ApplicationStatus,
	} from '$interfaces/application'

	const { receive } = $as

	function getApplicationStatus(app: Application): ApplicationStatus {
		if (app.application_processed) {
			return {
				label: 'Awaiting Review',
				percent: 100,
				color: 'bg-green-400',
			}
		}

		if (app.application_processing) {
			return {
				label: 'In progress',
				percent: 66,
				color: 'bg-orange-400',
			}
		}

		if (app.application_requested) {
			return {
				label: 'Pending',
				percent: 33,
				color: 'bg-orange-800',
			}
		}

		return {
			label: 'Unknown',
			percent: 0,
			color: 'bg-gray-400',
		}
	}

	$: $as.applications.forEach((app) => {
		app.progress = getApplicationStatus(app) as ApplicationStatus
	})
</script>

<div id="container" class="hidden md:flex min-w-[20rem]">
	<div
		class="text-center p-2 text-xl font-medium text-white bg-amber-800">
		My Applications
	</div>
	<ul class="overflow-y-auto overflow-x-hidden flex-grow p-0">
		{#if !$as.applications.length}
			<div class="text-white text-xl h-full flex flex-col justify-center items-center">
				<div class="flex flex-col items-center font-light pb-20">
					<Icon height="6em" inline={false} icon="ion:file-tray"/>
					No Applications Yet
				</div>
			</div>
		{/if}
		{#each $as.applications as app (app._id)}
			<a href={"/jobs/" + app.job_id}>
				<li in:receive={{ key: app._id }}>
					<div class="text-lg font-bold">{app.job.company.name}</div>
					<div class="text-sm font-light">{app.job.role}</div>
					<div class="flex items-center">
						{#if app.progress}
							<div class="h-3 w-3/5 border-2 rounded-full">
								<div
									class="{app.progress.color} h-full rounded-full"
									style="width: {app.progress.percent}%" />
							</div>
							<div class="text-sm w-2/5 ml-1">
								{app.progress.label}
							</div>
						{/if}
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
