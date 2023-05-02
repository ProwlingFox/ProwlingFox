import { get } from '$lib/requestUtils'


export async function load({ fetch }) {
    const metrics = await get('/admin/metrics', fetch)

    return {
        metrics: metrics
    }
}
