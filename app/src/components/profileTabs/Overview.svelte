<script lang="ts">
	import type { User } from "$interfaces/user"
    export let userInfo: User

    import { Avatar } from "flowbite-svelte"
</script>

<div class="p-8 py-6 md:p-12 md:py-8 flex justify-between w-full bg-amber-100 h-min">
    <div class="self-end">
        <div class="text-4xl font-semibold">{userInfo.name}</div>
        <div>{userInfo.email}</div>
    </div>
    <div>
        <Avatar class="h-28 w-28 md:h-36 md:w-36" size="xl" src={userInfo.picture}/>
    </div>
</div>
