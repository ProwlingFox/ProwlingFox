import { get } from '$lib/requestUtils'


export async function load({ fetch }) {
    const metrics =  get('/admin/metrics', fetch)
    const users = get('/admin/users')

    return {
        metrics: await metrics,
        users: await users
    }
}
