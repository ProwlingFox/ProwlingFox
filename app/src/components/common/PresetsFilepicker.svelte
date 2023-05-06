<script lang="ts">
	import { parseJWT } from '$lib/requestUtils'
    import Icon from '@iconify/svelte'
    import { Dropdown, DropdownItem, DropdownDivider, DropdownHeader, Chevron, Button, Dropzone, Modal } from 'flowbite-svelte'

    export let id: string
    export let required: boolean
    export let disabled: boolean
    export let content: string
    export let file: {
        file_name: string
        data: string
    }
    let files: FileList
    let fileModal = false
    let dropdownOpen = false

    export let defaultOptions: {
        fileName: string
        presetID: string
    }[]

    const blobToData = (blob: Blob) => {
        return new Promise<string>((resolve) => {
            const reader = new FileReader()
            reader.onloadend = () => {
                if (typeof(reader.result) === "string") {
                    resolve(reader.result)
                }
            }
            reader.readAsDataURL(blob)
        })
    }

    async function fileUpload() {
        fileModal = false
        const fileData = await blobToData(files[0])
        file = {
            file_name: files[0].name,
            data: fileData
        }
    }

    function setPresetFile(fileName: string, fileType: string) {
        dropdownOpen = false
        const userId = parseJWT()?.user_id
        file = {
            file_name: fileName,
            data: `preset:${userId},${fileType}`
        }
    }
</script>

<label for={id} data-required={required}>{content}</label>
<div class="w-full relative">
    {#if disabled}
        <div class="w-full p-1.5 text-left bg-white text-black border-solid border-2 border-gray-300 rounded-lg focus:border-gray-900 hover:bg-slate-200">FileName: {file?.file_name ?? "No File Sent"}</div>
    {:else}
    <Button btnClass="w-full p-1.5 text-left bg-white text-black border-solid border-2 border-gray-300 rounded-lg focus:border-gray-900 hover:bg-slate-200">
        {file?.file_name ?? "Select A File"}
    </Button>
    <Dropdown bind:open={dropdownOpen} class="w-full" frameClass="w-full">
        {#each defaultOptions as option}
            <DropdownItem on:click={() => {setPresetFile(option.fileName, option.presetID)}}>{option.fileName}</DropdownItem>
        {/each}
        <DropdownItem on:click={() => {fileModal = true}}>Upload Custom File</DropdownItem>
    </Dropdown>
    {/if}
</div>


<Modal class="w-[50vw] p-4" bind:open={fileModal} autoclose>
    <Dropzone id="fileDropzone" bind:files on:change={fileUpload}>
        <Icon height="8em" icon="solar:cloud-upload-linear"/>
        <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to upload</span> or drag and drop</p>
    </Dropzone>
</Modal>