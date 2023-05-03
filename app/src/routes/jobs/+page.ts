import type { Job } from '$interfaces/job.js'
import { get, getJWT } from '$lib/requestUtils'

export async function load({ fetch }) {
    const {jobs, totalJobs} = await get('/jobs')
	const j: Job[] = jobs

    return {
        jobs: j
    }
}
