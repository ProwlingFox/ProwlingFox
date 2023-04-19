import { writable, get as getStore } from 'svelte/store';
import { crossfade as svelteCrossfade } from 'svelte/transition';
import { get } from './requestUtils';
import type { Job } from '$interfaces/job';

const [send, receive] = svelteCrossfade({duration: 400});

interface Application {
    id: string
    companyName: string
    role: string
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


export const applications = writable<ApplicationStore>({
    applications: [],
    send,
    receive
});