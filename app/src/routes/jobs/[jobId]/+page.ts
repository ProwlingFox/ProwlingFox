import { get } from '$lib/requestUtils'
import { getApplicationByJobID } from '$lib/applications.js'

interface LoadParams {
	jobId: string
}

export async function load({ params, fetch }) {
	const jobId = params.jobId
	console.log("JobID:", jobId)
	let job = get('/jobs/' + jobId, fetch)

	let relatedApplication = getApplicationByJobID(jobId)

	return {
		job: await job,
		relatedApplication: await relatedApplication
	}
}
