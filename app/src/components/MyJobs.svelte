<script lang="ts">
	import { applications as as } from '$lib/myJobs'
	import type {
		Application,
		ApplicationStatus,
	} from '$interfaces/application'

	const { receive } = $as

	console.log($as)

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

<div class="w-1/5 h-100% bg-[#cb642c]">
	<div
		class="text-center p-4 text-xl font-medium text-white border-b-2 border-cyan-950">
		My Applications
	</div>
	<ul>
		{#each $as.applications as app (app.id)}
			<a href={"/jobs/" + app.job_id}>
				<li in:receive={{ key: app.id }}>
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
	li {
		@apply bg-white p-2 m-2 rounded-md shadow;
	}
</style>
