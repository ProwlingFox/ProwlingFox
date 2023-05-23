<script lang="ts">
	import { type Application, ApplicationStatus } from "$interfaces/application"
	import { post } from "$lib/requestUtils"
    import { Dropdown, DropdownItem, Button, DropdownDivider, Chevron } from 'flowbite-svelte'

    export let application: Application

    function getApplicationState(application: Application) {
        if (application.status == ApplicationStatus.Accepted) return "Offer Accepted"
        if (application.status == ApplicationStatus.Offered) return "Offer Received"
        if (application.status == ApplicationStatus.Interviewing) return "Interviewing"
        if (application.status == ApplicationStatus.Contact) return "Contacted"
        if (application.status == ApplicationStatus.Sent) return "Applied"
        if (application.status == ApplicationStatus.Rejected) return "Rejected"
        return "Select State"
    }


    function updateState(stateToUpdateTo: ApplicationStatus) {
        application.status = stateToUpdateTo
        post(`/applications/${application._id}/setstate`, {state: application.status})
    }
</script>

<div class="bg-white p-4 my-2 mr-4 w-80 h-52 shadow rounded-xl flex flex-col">
    <a href={"/jobs/" + application.job_id}>
        <div class="text-xl">{application.job.role}</div>
        <div class="font-light">at {application.job.company.name}</div>    
    </a>

    <button on:click|preventDefault class="flex items-center mt-auto ml-auto">{getApplicationState(application)}<Chevron/></button>
    <Dropdown>
        <DropdownItem on:click={() => {updateState(ApplicationStatus.Sent)}}>Applied</DropdownItem>
        <DropdownItem on:click={() => {updateState(ApplicationStatus.Contact)}}>Contacted By Company</DropdownItem>
        <DropdownItem on:click={() => {updateState(ApplicationStatus.Interviewing)}}>Interviewing</DropdownItem>
        <DropdownItem on:click={() => {updateState(ApplicationStatus.Offered)}}>Offer Received</DropdownItem>
        <DropdownItem on:click={() => {updateState(ApplicationStatus.Accepted)}}>Offer Accepted</DropdownItem>
        <DropdownDivider/>
        <DropdownItem on:click={() => {updateState(ApplicationStatus.Rejected   )}} class="text-red-700">Rejected</DropdownItem>
    </Dropdown>
</div>