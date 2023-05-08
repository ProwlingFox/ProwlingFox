import { get } from "./requestUtils"
import { get as getStore } from "svelte/store"
import { applications } from "./myJobs"
import { userData } from "./userData"

export async function getApplicationByJobID(jobId: string) {
	// Check if it's in the application store
	let relatedApplication =  getStore(applications).applications.find(x => x.job_id == jobId)
	// If Not, Pull It from the Backend
	if (!relatedApplication) {
		relatedApplication = await get("/user/applications/" + jobId)
	}
	return relatedApplication
}

export function parsePreformattedResponse(preformattedResponse: string) {
	if(!getStore(userData).data) {return}
	for (const [key, value] of Object.entries(getStore(userData).data)) {
		preformattedResponse = preformattedResponse.replace("{" + key + "}", String(value.Text))
	}

	// Email is a special case, Potentially replaced later as an email aggregator
	preformattedResponse = preformattedResponse.replace("{email}", String(getStore(userData).email))
	return preformattedResponse
}
