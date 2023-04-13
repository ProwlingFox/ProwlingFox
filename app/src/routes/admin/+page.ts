import { get } from '$lib/requestUtils'


export async function load({}) {
    const metrics = await get('/admin/metrics')

    return {
        metrics: metrics
    }
}
