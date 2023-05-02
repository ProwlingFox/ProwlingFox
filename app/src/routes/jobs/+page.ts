import { get, getJWT } from '$lib/requestUtils'


export async function load({ fetch }) {
    const jobs = await get('/jobs', fetch)

    return {
        jobs: jobs
    }
}
