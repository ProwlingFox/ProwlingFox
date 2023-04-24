import { writable, get as getStore } from 'svelte/store'
import { crossfade as svelteCrossfade } from 'svelte/transition'
import { get, getJWT } from './requestUtils'
import type { Job } from '$interfaces/job'
import type { ApplicationStore } from '$interfaces/application'
import { browser } from '$app/environment'

const [send, receive] = svelteCrossfade({ duration: 400 })

export const jobQueue = writable<string[]>([])

export async function popNextJobID() {
	if (getStore(jobQueue).length > 0) {
		const id = getStore(jobQueue)[0]
		jobQueue.update((x) => x.splice(1))
		return id
	} else {
		const newJobs: Job[] = await get('/jobs')
		jobQueue.set(newJobs.map((j) => j._id))
		const id = getStore(jobQueue)[0]
		jobQueue.update((x) => x.splice(1))
		return id
	}
}

function refreshApplications(buypassCheck: boolean = false) {
	if (!buypassCheck) {
		let moveableStates = getStore(applications).applications.some(x => !x.application_processed
			)
		console.log(moveableStates)
		if (!moveableStates) {
			return
		}
	}

	get('/user/applications').then((res) => {
		applications.update((a) => {
			return {
				applications: res,
				send: send,
				receive: receive,
			}
		})
	})
}

if(browser) {
	var intervalId = window.setInterval(refreshApplications, 10000);
}
refreshApplications(true)

export const applications = writable<ApplicationStore>({
	applications: [],
	send,
	receive,
})
