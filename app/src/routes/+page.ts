import type { Application } from '$interfaces/application.js'
import { get } from '$lib/requestUtils'

export async function load({ fetch }) {
    const applications: Application[] = await get('/user/applications', fetch, {"showSent": true})

    return {
        fullApplications: applications
    }
}
