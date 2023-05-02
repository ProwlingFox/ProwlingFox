<script lang="ts">
    import { Dropdown, DropdownItem, Button, Chevron, Search, Checkbox } from 'flowbite-svelte'

    import type { Role, User } from "$interfaces/user"
	import { get, post } from "$lib/requestUtils"
    export let userInfo: User
    
    const WHITELISTED_SECTORS = ["IT and Digital Technology"]
    const sectors: {[key: string]: {[key: string]: boolean} } = {}

    async function getRoles() {
        const roles: Role[] = await get("/roles")
        for(let role of roles){
            if (!WHITELISTED_SECTORS.includes(role.sector)) {continue}
            if (!sectors[role.sector]) { sectors[role.sector] = {} }
            sectors[role.sector][role.role] = false
        }
        for(let userRole of userInfo.job_preferences.roles) {
            sectors[userRole.sector][userRole.role] = true
        }
    }

    function addOrRemoveRole(sector: string, role: string, checked?: boolean) {    
        if (checked || !sectors[sector][role]) {
            userInfo.job_preferences.roles.push({
                "role": role,
                "sector": sector
            })
            userInfo.job_preferences.roles = userInfo.job_preferences.roles
        } else {
            userInfo.job_preferences.roles = userInfo.job_preferences.roles.filter(x => x.role !== role)
        }
        if (checked !== undefined) {
            sectors[sector][role] = checked
        }
        
        post('/user/update', userInfo)
    }

    getRoles()

</script>

<h4 class="my-2 mx-4 text-lg font-bold">My Active Searches</h4>
<div class="mx-4 flex flex-wrap">
    {#each userInfo.job_preferences.roles as role}
        <Button
            on:click={() => {addOrRemoveRole(role.sector, role.role, false)}}
            btnClass="m-1 p-2 px-4 bg-orange-400 rounded-xl text-white"
        >
            <div class="text-md">{role.role}</div>
            <div class="text-xs font-light">{role.sector}</div>
        </Button>
    {/each}
    <Button btnClass="m-1 p-2 px-4 bg-orange-700 rounded-xl text-white flex items-center"><Chevron>Add New Search</Chevron></Button>

    <Dropdown class="overflow-y-auto px-3 pb-3 text-sm max-h-[20rem]">
    <div slot="header" class="p-3">
        <Search size="md"/>
    </div>
    {#each Object.keys(sectors) as sector}
        <DropdownItem class="flex items-center justify-between hover:bg-orange-100"><Chevron placement="right">{sector}</Chevron></DropdownItem>
        <Dropdown placement="right-start" class="overflow-y-auto px-3 pb-3 text-sm max-h-[20rem]">
            {#each Object.keys(sectors[sector]) as role}
                <DropdownItem defaultClass="pl-2 hover:bg-orange-100">
                    <Checkbox color="orange" bind:checked={sectors[sector][role]} on:click={(e) => addOrRemoveRole(sector, role)}>
                        <div class="p-2">{role}</div>
                    </Checkbox>
                </DropdownItem>
            {/each}
        </Dropdown>
    {/each}
    </Dropdown>
</div>
<div>
    
</div>
