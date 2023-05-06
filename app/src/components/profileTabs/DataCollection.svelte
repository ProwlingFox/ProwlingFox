<script lang="ts">
    import type { User } from "$interfaces/user"
	import { post } from "$lib/requestUtils"
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

    async function inputBlur(e: FocusEvent) {

        post('/user/update', userInfo)
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

    for(const [key, value] of Object.entries(userInfo.data)){
        console.log(key, value)
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
                {#each Object.keys(userInfo.data) as key}
                    {#if typeof(userInfo.data[key]) == "object" && userInfo.data[key]}
                    <div class="display flex flex-col w-full sm:w-60 p-2 bg-orange-400 rounded-xl shadow-sm">
                            <label class="leading-0 font-normal text-white" for={key}>{getTitle(key)}</label>
                            FILE NOT IMPLEMENTED
                        </div>
                    {:else}
                        <div class="display flex flex-col w-full sm:w-60 p-2 bg-orange-400 rounded-xl shadow-sm">
                            <label class="leading-0 font-normal text-white" for={key}>{getTitle(key)}</label>
                            <input class="" id={key} on:blur={inputBlur} bind:value={userInfo.data[key]}>
                        </div>
                    {/if}
                {/each}
            </div>
        </div>
    </div>
</div>

<style lang="postcss">
    input{
        @apply border-solid border-2 border-orange-300 rounded-lg mb-2 pl-2;
    }

    input:focus{
        @apply border-gray-900;
    }
</style>