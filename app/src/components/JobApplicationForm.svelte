<script lang="ts">
	import type { Application as JobApplication } from "$interfaces/application"
	import type { Job } from "$interfaces/job"

    export let srcApplication: JobApplication | undefined
    export let srcJob: Job

</script>

<div id="questions">
    <h2 class="w-full absolute top-0 text-center right-0 text-xl rounded-t-xl font-semibold p-4">Application Review</h2>
    {#each srcJob.questions as question }
        {#if question.type == "Text"}
            <label for={question.id}>{question.content}</label>
            <input id={question.id} value={ srcApplication?.responses[question.id] || '' }/>
        {:else if question.type == "LongText"}
            <label for={question.id}>{question.content}</label>
            <textarea id={question.id} value={srcApplication?.responses[question.id] || ''}/>
        {:else if question.type == "Number"}
            <label for={question.id}>{question.content}</label>
            <input id={question.id} type="number" value={srcApplication?.responses[question.id] || ''}/>
        {:else if question.type == "MultipleChoice"}
            <label for={question.id}>{question.content}</label>
            <input id={question.id} value={srcApplication?.responses[question.id] || ''}/>
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
            <label for={question.id}>{question.content}</label>
            <input id={question.id} value={srcApplication?.responses[question.id] || ''}/>
        {/if}
    {/each}
    <button class="bg-green-400 self-end">Send Application</button>
</div>

<style lang="postcss">
    #questions {
        @apply bg-white max-w-2xl my-4 p-12 rounded-xl shadow-md relative right-4 flex flex-col;
    }

    input, textarea {
        @apply border-solid border-2 rounded-lg mb-2;
    }
</style>