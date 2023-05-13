import { writable, get as getStore } from 'svelte/store'
import { crossfade as svelteCrossfade } from 'svelte/transition'
import { get, getJWT } from './requestUtils'
import type { Job } from '$interfaces/job'
import type { ApplicationStore } from '$interfaces/application'
import { browser } from '$app/environment'

const [send, receive] = svelteCrossfade({ duration: 400 })

export const jobQueue = writable<string[]>([])
export const userJobsLeft = writable<number>(0)
export const userJobTags = writable<string[]>([])

export function invalidateJobQueue() {
	jobQueue.set([])
}

export async function popNextJobID() {
	if (getStore(jobQueue).length > 0) {
		const id = getStore(jobQueue)[0]
		jobQueue.update((x) => x.splice(1))
		return id
	} else {
		const {jobs, totalJobs} = await get('/jobs')
		const newJobs: Job[] = jobs
		if (!newJobs?.length) return null
		jobQueue.set(newJobs.map((j) => j._id))
		const id = getStore(jobQueue)[0]
		jobQueue.update((x) => x.splice(1))
		userJobsLeft.set(totalJobs)
		let roles: {[key: string]: number} = {}
		for (let job of newJobs) {
			for (let role of job.role_category) {
				if (!(role in roles)) {roles[role] = 0}
				roles[role] += 1
			}
		}
		userJobTags.set(Object.keys(roles).sort((a, b) => roles[b] - roles[a]))
		return id
	}
}

export async function refreshApplications(buypassCheck: boolean = false) {
	if (!buypassCheck) {
		// Checks to see if applications could change state, if not doesn't send a needless web request
		let moveableStates = getStore(applications).applications.some(
			(x) => !( (x.application_processed && !x.application_reviewed) || (x.application_sent) )
		)
		if (!moveableStates) {
			return
		}
	}

	await get('/user/applications').then((res) => {
		applications.update((a) => {
			return {
				applications: Array.isArray(res) ? res : [],
				send: send,
				receive: receive,
			}
		})
	})
}

if (browser) {
	var intervalId = window.setInterval(refreshApplications, 5000)
}

export const applications = writable<ApplicationStore>({
	applications: [],
	send,
	receive,
})

refreshApplications(true)