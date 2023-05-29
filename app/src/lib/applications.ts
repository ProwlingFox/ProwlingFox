import { get } from "./requestUtils"
import { get as getStore } from "svelte/store"
import { applications } from "./myJobs"
import { userData } from "./userData"
import type { UserFile } from "$interfaces/user"

export async function getApplicationByJobID(jobId: string) {
	let relatedApplication = await get("/applications/" + jobId)

	if (!relatedApplication || !("_id" in relatedApplication)) {return undefined}

	return relatedApplication
}

export function parsePreformattedResponse(preformattedResponse: string, questionType: string) {
	if(!getStore(userData).data) {return}

	// String Case
	if (questionType == "Text") {
		for (const [key, value] of Object.entries(getStore(userData).data)) {
			preformattedResponse = preformattedResponse.replace("{" + key + "}", String(value.Text))
		}
		// Email is a special case, Potentially replaced later as an email aggregator
		preformattedResponse = preformattedResponse.replace("{email}", String(getStore(userData).email))
		return preformattedResponse
	}

	// String Case Is The Only Case That Can contain multiple {}{} so now we can just strip back to var
	preformattedResponse = preformattedResponse.substring(1, preformattedResponse.length-1)

	// Number Case
	if (questionType == "Number") {
		return getStore(userData).data[preformattedResponse]?.Number
	}

	if (questionType == "File") {
		let file: UserFile = {
			file_name: getStore(userData).data[preformattedResponse]?.File?.file_name ?? "",
			data: `preset:${getStore(userData)._id},${preformattedResponse}`
		}
		return file.file_name ? file : undefined
	}

	
	return 
}
