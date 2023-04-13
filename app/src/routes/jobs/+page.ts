import { get } from '$lib/requestUtils'


export async function load({  }) {
    const jobs = await get('/jobs')

    return {
        jobs: jobs
    }
}
