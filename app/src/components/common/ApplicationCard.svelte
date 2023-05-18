<script lang="ts">
	import type { Application } from "$interfaces/application"
    import { Dropdown, DropdownItem, Button, DropdownDivider, Chevron } from 'flowbite-svelte'

    export let application: Application

    function getApplicationState(application: Application) {
        if (application.application_accepted) return "Offer Accepted"
        if (application.application_offer) return "Offer Received"
        if (application.application_interview) return "Interviewing"
        if (application.application_contact) return "Contacted"
        if (application.application_sent) return "Applied"
        if (application.application_rejected) return "Rejected"
        return "Select State"
    }


    function updateState(stateToUpdateTo: string) {
        switch (stateToUpdateTo) {
            case "Rejected":
                application.application_rejected = true
                break;
            case "Offer":
                application.application_offer = true
            case "Interviewing":
                application.application_interview = true
            case "Contacted":
                application.application_contact = true
            case "Applied":
                application.application_sent = true
        }
        switch (stateToUpdateTo) {
            case "Applied":
                application.application_contact = false
            case "Contacted":
                application.application_interview = false
            case "Interviewing":
                application.application_offer = false
            case "Offer":
                application.application_rejected = false
        }
        console.log(application)
    }
</script>

<div class="bg-white p-4 my-2 mr-4 w-80 h-52 shadow rounded-xl flex flex-col">
    <a href={"/jobs/" + application.job_id}>
        <div class="text-xl">{application.job.role}</div>
        <div class="font-light">at {application.job.company.name}</div>    
    </a>

    <button on:click|preventDefault class="flex items-center mt-auto ml-auto">{getApplicationState(application)}<Chevron/></button>
    <Dropdown>
        <DropdownItem on:click={() => {updateState("Applied")}}>Applied</DropdownItem>
        <DropdownItem on:click={() => {updateState("Contacted")}}>Contacted By Company</DropdownItem>
        <DropdownItem on:click={() => {updateState("Interviewing")}}>Interviewing</DropdownItem>
        <DropdownItem on:click={() => {updateState("Offer")}}>Offer Received</DropdownItem>
        <DropdownDivider/>
        <DropdownItem on:click={() => {updateState("Rejected")}} class="text-red-700">Rejected</DropdownItem>
    </Dropdown>
</div>