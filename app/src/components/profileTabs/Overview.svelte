<script lang="ts">
	import type { User } from "$interfaces/user"
    export let userInfo: User

    import { Avatar } from "flowbite-svelte"
</script>

<div class="p-12 py-8 flex justify-between w-full bg-amber-100 h-min">
    <div class="self-end">
        <div class="text-4xl font-semibold">{userInfo.name}</div>
        <div>{userInfo.email}</div>
    </div>
    <div>
        <Avatar size="xl" src={userInfo.picture}/>
    </div>
</div>
