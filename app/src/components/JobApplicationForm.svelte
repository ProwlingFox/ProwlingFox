<script lang="ts">
	import type { Application as JobApplication } from "$interfaces/application"
	import type { Job } from "$interfaces/job"

    export let srcApplication: JobApplication | undefined
    export let srcJob: Job

</script>

<div class=" md:mx-4 lg:mx-0 lg:max-w-2xl bg-white my-4 sm:p-12 sm:rounded-xl shadow-xl relative lg:right-4 flex flex-col">
    <h2 class="w-full absolute top-0 text-center right-0 text-xl rounded-t-xl font-semibold p-4">Application Review</h2>
    {#each srcJob.questions as question }
        {#if question.type == "Text"}
            <label for={question.id}>{question.content}</label>
            <input id={question.id} value={ srcApplication?.responses[question.id] || '' }/>
        {:else if question.type == "LongText"}
            <label for={question.id}>{question.content}</label>
            <textarea id={question.id} rows="8" value={srcApplication?.responses[question.id] || ''}/>
        {:else if question.type == "Number"}
            <label for={question.id}>{question.content}</label>
            <input id={question.id} type="number" value={srcApplication?.responses[question.id] || ''}/>
        {:else if question.type == "MultipleChoice" && question.choices}
            <label for={question.id}>{question.content}</label>
            <select id={question.id}>
                {#each question.choices as choice}
                    <option value={choice.id}>{choice.content}</option>
                {/each}
            </select>
            <!-- <input  value={srcApplication?.responses[question.id] || ''}/> -->
        {:else if question.type == "Date"}
            <label for={question.id}>{question.content}</label>
            <input id={question.id} type="date" value={srcApplication?.responses[question.id] || ''}/>
        {:else if question.type == "File"}
            <label for={question.id}>{question.content}</label>
            <input id={question.id} type="file"/>
        {:else if question.type == "CheckBox"}
            <label for={question.id}>{question.content}</label>
            <input id={question.id} type="checkbox" value={srcApplication?.responses[question.id] || ''}/>
        {:else if question.type == "Radio"}
            <label for={question.id}>{question.content} (Radio)</label>
            <input id={question.id} value={srcApplication?.responses[question.id] || ''}/>
        {/if}
    {/each}
    <button class="bg-green-400 self-end">Send Application</button>
</div>

<style lang="postcss">
    input, textarea, select{
        @apply border-solid border-2 border-gray-300 rounded-lg mb-2 pl-2;
    }

    button {
        @apply p-2 w-40 rounded-xl drop-shadow text-white;
    } 

    input:focus, textarea:focus, select:focus{
        @apply border-gray-900;
    }
</style>