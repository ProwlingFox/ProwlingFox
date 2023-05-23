import type { Application } from '$interfaces/application.js'
import type { UserStats } from '$interfaces/user.js'
import { get } from '$lib/requestUtils'

export async function load({ fetch }) {
    const applications: Promise<Application[]> =  get('/applications', fetch, {"showSent": true})
    const userStats: Promise<UserStats> =  get('/user/metrics', fetch, {"showSent": true})

    return {
        fullApplications: await applications,
        stats: await userStats
    }
}
