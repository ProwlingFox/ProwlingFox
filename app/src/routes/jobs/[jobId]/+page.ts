import { get } from '$lib/requestUtils'

interface LoadParams {
	jobId: string
}


export async function load({ params }: { params: LoadParams }) {
	// const jobId = params.jobId
	return { jobId: params.jobId }

	// let job
	// get('/jobs/' + jobId).then((res) => {
	// 	job = res
	// 	console.log(job)
	// })
}
