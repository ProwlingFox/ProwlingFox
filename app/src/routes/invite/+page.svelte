<script lang="ts">
	import { saveUserData, userData } from "$lib/userData"

    async function emailOptOut(optOut: boolean) {
        $userData.email_opt_out = optOut
        saveUserData()
        return
    }
</script>

<div class="flex flex-col max-w-md self-center pb-40 m-8 lg:m-auto text-center">
    <h2 class="text-2xl font-bold w-full mb-2 text-amber-900">Thanks for your interest!</h2>
    <p class="">
        ProwlingFox is currently in beta access, we are excited to share it with you soon.
        If you have been given access to the beta, please wait a little bit for your account to be activated.
    </p>

    {#if $userData.email_opt_out}
        <button class="font-light text-sm text-orange-600 mt-1 pt-2 border-t border-dashed border-orange-200" on:click={() => emailOptOut(false)}>Opt into email communication.</button>
    {:else}
        <button class="font-light text-sm text-orange-600 mt-1 pt-2 border-t border-dashed border-orange-200" on:click={() => emailOptOut(true)}>Opt out of email communication.</button>
    {/if}
</div>