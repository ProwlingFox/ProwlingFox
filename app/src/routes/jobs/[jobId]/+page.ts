import { get } from '$lib/requestUtils'
import { getApplicationByJobID, parsePreformattedResponse } from '$lib/applications.js'
import type { Job } from '$interfaces/job.js'
import type { Application } from '$interfaces/application.js'

interface LoadParams {
	jobId: string
}


async function loadFromUserdata(job: Job, application: Application | undefined) {
	if(!application || !application.application_processed) {return application}
	for (const question of job.questions) {
		if (!question.response) {continue}
		application.responses[question.id] = parsePreformattedResponse(question.response)
	}
	return application
}

export async function load({ params, fetch }) {
	const jobId = params.jobId
	console.log("JobID:", jobId)
	let job = get('/jobs/' + jobId, fetch)

	let relatedApplication = await getApplicationByJobID(jobId)
	relatedApplication = await loadFromUserdata(await job, relatedApplication)

	return {
		job: await job,
		relatedApplication: await relatedApplication
	}
}
