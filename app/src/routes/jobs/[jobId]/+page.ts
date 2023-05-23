import { get } from '$lib/requestUtils'
import { getApplicationByJobID, parsePreformattedResponse } from '$lib/applications.js'
import { invaldateUserData, userData } from '$lib/userData.js'
import { get as getStore } from 'svelte/store'

import type { Job } from '$interfaces/job.js'
import { ApplicationStatus, type Application } from '$interfaces/application.js'

interface LoadParams {
	jobId: string
}


async function loadFromUserdata(job: Job, application: Application | undefined) {
	if(!application || 
		application.status != ApplicationStatus.Processed ||
		!application.responses
	) {return application}
	for (const question of job.questions) {
		if (!question.response) {continue}
		application.responses[question.id] = parsePreformattedResponse(question.response, question.type)
	}
	return application
}

export async function load({ params, fetch }) {
	if (params.jobId == "complete") {
		return
	}

	const jobId = params.jobId
	console.log("JobID:", jobId)
	let job = get('/jobs/' + jobId, fetch)

	if(!getStore(userData)) {
		await invaldateUserData()
	}

	let relatedApplication = await getApplicationByJobID(jobId)
	relatedApplication = await loadFromUserdata(await job, relatedApplication)

	return {
		job: await job,
		relatedApplication: await relatedApplication
	}
}
