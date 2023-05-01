import { get } from '$lib/requestUtils'

interface LoadParams {
	jobId: string
}


export async function load({ params }: { params: LoadParams }) {
	const jobId = params.jobId
	console.log("JobID:", jobId)
	let job = await get('/jobs/' + jobId)

	return {
		job: job
	}
}
