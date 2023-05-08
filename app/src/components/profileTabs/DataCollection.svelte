<script lang="ts">
    import type { User } from "$interfaces/user"
	import { post } from "$lib/requestUtils"
	import { invaldateUserData } from "$lib/userData"
    import { Fileupload } from 'flowbite-svelte'
    export let userInfo: User

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

    async function fileBlur(e: FocusEvent, var_name: string) {
        if (!(e.target && "files" in e.target)) {return}
        if (!(e.target.files instanceof FileList)) {return} 
        if (e.target.files.length < 1) {return}

        const file = e.target.files[0]
        const b64File = await blobToData(file)

        userInfo.data[var_name].File = {
            file_name: file.name,
            data: b64File
        }

        inputBlur(e)
    }

    async function inputBlur(e: FocusEvent) {
        post('/user/update', userInfo)
        invaldateUserData()
    }

    const userDataKeyTranslation: {[key: string]: string} =  {
        firstname: "First Name",
        surname: "Last Name",
        website: "Personal Website/Portfolio",
        git: "Github/Bitbucket/etc...",
        linkedIn: "LinkedIn",
        phone_number: "Phone Number",
        pronouns: "Prefered Pronouns",
        notice_period: "Notice Period",
        expected_sallary: "Sallary Expectation",
        address: "Current Address",
        resume: "Resume"
    }
    
    function getTitle(key: string) {
        return userDataKeyTranslation[key] ?? key
    }
</script>

<div class="m-4">
    <h3 class="text-2xl">My Data</h3>
    <p class="font-thin mx-1 text-justify">In order to answer applications as accurately as possible we collect and analyse data from every application you send.
        The more accurate and complete the data below, the better we can apply to open positons.</p>
    <div class="flex flex-col">
        <div>
            <h3 class="text-xl font-bold mt-4">Basic Information</h3>
            <div class="flex gap-4 flex-wrap">
                {#each Object.keys(userInfo.data) as var_name}
                    {#each Object.keys(userInfo.data[var_name]) as var_type}
                        {#if var_type == "Text"}
                            <div class="display flex flex-col w-full sm:w-60 p-2 bg-orange-400 rounded-xl shadow-sm">
                                <label class="leading-0 font-normal text-white" for={var_name}>{getTitle(var_name)} ({var_type})</label>
                                <input type="text" id={var_name} on:blur={inputBlur} bind:value={userInfo.data[var_name][var_type]}>
                            </div>
                        {:else if var_type == "Number"}
                            <div class="display flex flex-col w-full sm:w-60 p-2 bg-orange-400 rounded-xl shadow-sm">
                                <label class="leading-0 font-normal text-white" for={var_name}>{getTitle(var_name)} ({var_type})</label>
                                <input type="number" id={var_name} on:blur={inputBlur} bind:value={userInfo.data[var_name][var_type]}>
                            </div>
                        {:else if var_type == "Date"}
                            <div class="display flex flex-col w-full sm:w-60 p-2 bg-orange-400 rounded-xl shadow-sm">
                                <label class="leading-0 font-normal text-white" for={var_name}>{getTitle(var_name)} ({var_type})</label>
                                <input type="date" id={var_name} on:blur={inputBlur} bind:value={userInfo.data[var_name][var_type]}>
                            </div>
                        {:else if var_type == "Checkbox"}
                            <div class="display flex flex-col w-full sm:w-60 p-2 bg-orange-400 rounded-xl shadow-sm">
                                <label class="leading-0 font-normal text-white" for={var_name}>{getTitle(var_name)} ({var_type})</label>
                                <input type="checkbox" id={var_name} on:blur={inputBlur} bind:value={userInfo.data[var_name][var_type]}>
                            </div>
                        {:else if var_type == "File"}
                            <div class="display flex flex-col w-full sm:w-60 p-2 bg-orange-400 rounded-xl shadow-sm">
                                <label class="leading-0 font-normal text-white" for={var_name}>{getTitle(var_name)} ({var_type})</label>
                                <button class="border-solid border-2 border-orange-300 rounded-lg mb-2 pl-2 p-2 bg-white focus:border-gray-900" on:click={(e) => {
                                    if(!(e.target instanceof HTMLElement && e.target.nextElementSibling instanceof HTMLElement)) {return}
                                    e.target.nextElementSibling.click()
                                }}>{userInfo.data[var_name][var_type]?.file_name || "Upload A File"}</button>
                                <input type="file" id={var_name} on:blur={e => fileBlur(e, var_name)} class="hidden">
                            </div>
                        {/if}
                    {/each}  
                {/each}
            </div>
        </div>
    </div>
</div>

<style lang="postcss">
    input{
        @apply border-solid border-2 border-orange-300 rounded-lg mb-2 pl-2 p-2 bg-white;
    }

    input:focus {
        @apply border-gray-900;
    }
</style>