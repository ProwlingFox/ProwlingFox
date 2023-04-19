import { writable, get as getStore } from 'svelte/store';
import { crossfade as svelteCrossfade } from 'svelte/transition';
import { get } from './requestUtils';
import type { Job } from '$interfaces/job';

const [send, receive] = svelteCrossfade({duration: 400});

interface Application {
    id: string,
    user_id?: string,
    job_id: string,
    job: Job,
    application_read: boolean,
    application_requested: boolean,
    application_processing: boolean,
    application_processed: boolean
}

interface ApplicationStore {
    applications: Application[],
    send: any,
    receive: any
}

export const jobQueue = writable<string[]>([])

export async function popNextJobID() {
    if (getStore(jobQueue).length > 0) {
        const id = getStore(jobQueue)[0]
        jobQueue.update(x => x.splice(1))
        return id
    } else {
        const newJobs: Job[] = await get("/jobs")
        jobQueue.set(newJobs.map(j => j.id))
        const id = getStore(jobQueue)[0]
        jobQueue.update(x => x.splice(1))
        return id
    }
}



get('/user/applications').then((res) => {
    applications.update((a) => {
        return {
            "applications": res,
            "send": send, 
            "receive": receive
        }
    })
})

export const applications = writable<ApplicationStore>({
    applications: [],
    send,
    receive
});