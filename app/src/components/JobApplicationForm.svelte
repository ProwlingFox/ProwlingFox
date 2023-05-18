<script lang="ts">
	import { goto } from "$app/navigation"
	import { ApplicationStatus, type Application as JobApplication } from "$interfaces/application"
	import type { Job } from "$interfaces/job"
	import { refreshApplications, applications, popNextJobID } from "$lib/myJobs"
	import { post } from "$lib/requestUtils"
	import Icon from "@iconify/svelte"
	import PresetsFilepicker from "./common/PresetsFilepicker.svelte"
    import { saveUserData, userData } from "$lib/userData"
	import { parsePreformattedResponse } from "$lib/applications"

    export let srcApplication: JobApplication
    export let srcJob: Job

    let presetFileTypes: {
        presetName: string
        fileName: string
        presetID: string
    }[] = []

    if ($userData.data.resume.File) {
        presetFileTypes.push({
            presetName: "Resume",
            fileName: $userData.data.resume.File?.file_name,
            presetID: "resume"
        })
    }

    async function updateUserData() {
        let changes = false
        for (const question of srcJob.questions) {
            if (!question.response) {continue}
            // TODO: Make sure file works proper
            if (question.type == "File") {continue}
            // If The Response Has Changed
            if (srcApplication.responses[question.id] != parsePreformattedResponse(question.response, question.type)) {
                const strippedResponse = question.response.substring(1, question.response.length-1)
                if (strippedResponse in $userData.data) {
                    changes = true
                    $userData.data[strippedResponse][question.type] = srcApplication.responses[question.id]
                }
            }
        }
        await saveUserData()
    }


    async function sendApplication() {
        await updateUserData()
        const resp = await post(`/jobs/${srcJob._id}/apply`, {
            responses: srcApplication.responses
        })
        refreshApplications(true)

        // Goto Next Application awaiting review or New Job
        let nextApplication = $applications.applications.findLast(x => x.status == ApplicationStatus.Processed && (x._id != srcApplication._id))
        if(nextApplication) {
            goto("/jobs/" + nextApplication.job_id)
        } else {
            goto("/jobs/" + await popNextJobID())
        }
    }

    async function rejectApplication() {
		await post(`/jobs/${srcJob._id}/mark`, { requestApply: false })
        refreshApplications(true)
        goto("/")
	}

</script>

<div class="pt-12 p-2 my-0 xl:min-w-[30em] xl:w-[40em] md:mx-4 lg:mx-0 lg:max-w-2xl bg-white sm:my-4 sm:p-12 sm:rounded-xl shadow-xl relative xl:right-4 flex flex-col">
    <h2 class="w-full absolute top-0 text-center right-0 text-xl rounded-t-xl font-semibold p-4">Application Review</h2>
    {#each srcJob.questions as question }
        {#if question.type == "Text"}
            <label for={question.id} data-required={question.required}>{question.content}</label>
            <input id={question.id} required={question.required} disabled={srcApplication.status >= ApplicationStatus.Reviewed} bind:value={srcApplication.responses[question.id]}/>
        {:else if question.type == "LongText"}
            <label for={question.id} data-required={question.required}>{question.content}</label>
            <textarea id={question.id} required={question.required} disabled={srcApplication.status >= ApplicationStatus.Reviewed} rows="8" bind:value={srcApplication.responses[question.id]}/>
        {:else if question.type == "Number"}
            <label for={question.id} data-required={question.required}>{question.content}</label>
            <input id={question.id} required={question.required} disabled={srcApplication.status >= ApplicationStatus.Reviewed} type="number" bind:value={srcApplication.responses[question.id]}/>
        {:else if question.type == "MultipleChoice" && question.choices}
            <label for={question.id} data-required={question.required}>{question.content}</label>
            <select id={question.id} required={question.required} disabled={srcApplication.status >= ApplicationStatus.Reviewed} bind:value={srcApplication.responses[question.id]}>
                {#each question.choices as choice}
                    <option value={choice.id}>{choice.content}</option>
                {/each}
            </select>
        {:else if question.type == "Date"}
            <label for={question.id} data-required={question.required}>{question.content}</label>
            <input id={question.id} type="date" required={question.required} disabled={srcApplication.status >= ApplicationStatus.Reviewed} bind:value={srcApplication.responses[question.id]}/>
        {:else if question.type == "File"}
            <PresetsFilepicker 
                id={question.id}
                required={question.required}
                disabled={srcApplication.status >= ApplicationStatus.Reviewed}
                content={question.content}
                defaultOptions={presetFileTypes}
                bind:file={srcApplication.responses[question.id]}
            />
        {:else if question.type == "CheckBox"}
            <label for={question.id} data-required={question.required}>{question.content}</label>
            <input id={question.id} required={question.required} disabled={srcApplication.status >= ApplicationStatus.Reviewed} type="checkbox" bind:checked={srcApplication.responses[question.id]}/>
        {:else if question.type == "Radio"}
            <label for={question.id} data-required={question.required}>{question.content} (Radio)</label>
            <input id={question.id} required={question.required} disabled={srcApplication.status >= ApplicationStatus.Reviewed} bind:value={srcApplication.responses[question.id]}/>
        {/if}
    {/each}
    {#if srcApplication.status == ApplicationStatus.Processed}
    <div class="flex justify-between">
        <button on:click={rejectApplication} class="bg-red-500 self-end w-auto px-2"><Icon height="1.5em" icon="fa:trash-o"/></button>
        <button on:click={sendApplication} class="bg-green-400 self-end w-40">Send Application</button>
    </div>
    {/if}
</div>

<style lang="postcss">
    input, textarea, select{
        @apply border-solid border-2 border-gray-300 rounded-lg mb-2 pl-2;
    }

    button {
        @apply p-2 rounded-xl drop-shadow text-white;
    } 

    input:focus, textarea:focus, select:focus{
        @apply border-gray-900;
    }

    input:required, textarea:required, select:required{
        /* @apply border-red-400; */
    }

    label[data-required="true"]::after {
        content: "*";
        color: red;
        
    }
</style>