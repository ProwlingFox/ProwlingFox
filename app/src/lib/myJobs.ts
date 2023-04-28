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
		if (!newJobs.length) return null
		jobQueue.set(newJobs.map((j) => j._id))
		const id = getStore(jobQueue)[0]
		jobQueue.update((x) => x.splice(1))
		return id
	}
}

async function refreshApplications(buypassCheck: boolean = false) {
	if (!buypassCheck) {
		// Checks to see if applications could change state, if not doesn't send a needless web request
		let moveableStates = getStore(applications).applications.some(
			(x) => !x.application_processed
		)
		if (!moveableStates) {
			return
		}
	}

	await get('/user/applications').then((res) => {
		applications.update((a) => {
			return {
				applications: res,
				send: send,
				receive: receive,
			}
		})
	})
}

if (browser) {
	var intervalId = window.setInterval(refreshApplications, 10000)
}

export const applications = writable<ApplicationStore>({
	applications: [],
	send,
	receive,
})

await refreshApplications(true)
