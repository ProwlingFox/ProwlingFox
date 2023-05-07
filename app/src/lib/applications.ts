import { get } from "./requestUtils"
import { get as getStore } from "svelte/store"
import { applications } from "./myJobs"

export async function getApplicationByJobID(jobId: string) {
	// Check if it's in the application store
	let relatedApplication =  getStore(applications).applications.find(x => x.job_id == jobId)
	// If Not, Pull It from the Backend
	if (!relatedApplication) {
		relatedApplication = await get("/user/applications/" + jobId)
	}
	return relatedApplication
}