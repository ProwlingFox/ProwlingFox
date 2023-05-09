<script lang="ts">
    import { Dropdown, DropdownItem, Button, Chevron, Search, Checkbox, Radio } from 'flowbite-svelte'

    import type { Role, User } from "$interfaces/user"
	import { get, post } from "$lib/requestUtils"
	import { invalidateJobQueue } from '$lib/myJobs'
	import type { CountryInfo } from '$interfaces/common'
	import type { RadioEvents } from 'flowbite-svelte/dist/forms/Radio.svelte'
    export let userInfo: User
    
    const WHITELISTED_SECTORS = ["IT and Digital Technology"]

    const sectors: {[key: string]: {[key: string]: boolean} } = {}
    let locations: CountryInfo[]

    let roleSearchQuery = ""
    let countrySearchQuery = ""
    let citySearchQuery = ""


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

    async function getLocations() {
        locations = await get("/locations")
    }

    async function updateCountry(e: Event) {
        if (!e.target) {return}
        const target = <HTMLInputElement>e.target
        const country_code = target.name
        const selection = target.value

        let country_preferences = userInfo.job_preferences.location.country_preferences
        country_preferences = country_preferences.filter(x => x.country_code != country_code)

        if (selection != "") {
            country_preferences.push({
                country_code: country_code,
                has_visa: selection == "hasvisa"
            })
        }

        userInfo.job_preferences.location.country_preferences = country_preferences
        sendUpdate()
    }

    async function updateCity(e: Event, country: string, city: string) {
        if (!e.target) {return}
        const target = <HTMLInputElement>e.target
        const checked = target.checked

        let city_preferences = userInfo.job_preferences.location.city_preferences

        city_preferences = city_preferences.filter(x => !(x.country == country && x.city == city))
        if (checked) {
            city_preferences.push({
                country: country,
                city: city
            })
        }

        userInfo.job_preferences.location.city_preferences = city_preferences
        sendUpdate()
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
        
        sendUpdate()
    }

    function sendUpdate() {
        post('/user/update', userInfo)
        // Invalidate Current Job Queue
        invalidateJobQueue()
    }

    getRoles()
    getLocations()
</script>

<h4 class="my-2 mx-4 text-lg font-bold">My Active Searches</h4>
<div class="mx-2 md:mx-4 flex flex-wrap">
    
    <Button btnClass="m-1 p-2 w-full md:w-auto px-4 justify-center bg-orange-700 rounded-xl text-white flex items-center"><Chevron>Add New Search</Chevron></Button>

    <Dropdown class="w-[95vw] md:w-auto overflow-y-auto px-3 pb-3 text-sm max-h-[20rem]">
    <div slot="header" class="p-3">
        <Search bind:value={roleSearchQuery} size="md"/>
    </div>
    <div class="empty:before:content-['Nothing_Matches_This_Search.'] before:pt-4 before:w-full empty:before:block">
    
    {#each Object.keys(sectors) as sector}
        {#if roleSearchQuery.length < 3}
            <DropdownItem class="flex items-center justify-between hover:bg-orange-100"><Chevron placement="right">{sector}</Chevron></DropdownItem>
            <Dropdown placement="bottom-start" class="w-[88vw] md:w-auto overflow-y-auto px-3 pb-3 text-sm max-h-[14rem] md:max-h-[20rem]">
            {#each Object.keys(sectors[sector]) as role}
                <DropdownItem defaultClass="pl-2 hover:bg-orange-100">
                    <Checkbox color="orange" bind:checked={sectors[sector][role]} on:click={(e) => addOrRemoveRole(sector, role)}>
                        <div class="p-2">{role}</div>
                    </Checkbox>
                </DropdownItem>
            {/each}
            </Dropdown>
        {:else}
            {#each Object.keys(sectors[sector]) as role}
                {#if role.toLowerCase().includes(roleSearchQuery.toLowerCase())}
                    <DropdownItem defaultClass="pl-2 hover:bg-orange-100">
                        <Checkbox color="orange" bind:checked={sectors[sector][role]} on:click={(e) => addOrRemoveRole(sector, role)}>
                            <div class="p-2">{role}</div>
                        </Checkbox>
                    </DropdownItem>
                {/if}
            {/each}
        {/if}
    {/each}
    </div>
    </Dropdown>
    {#each userInfo.job_preferences.roles as role}
        <Button
            on:click={() => {addOrRemoveRole(role.sector, role.role, false)}}
            btnClass="m-1 p-2 w-full md:w-auto px-2 md:px-4 bg-orange-400 rounded-xl text-white"
        >
            <div class="text-md">{role.role}</div>
            <div class="text-xs font-light">{role.sector}</div>
        </Button>
    {/each}
</div>


<h4 class="my-2 mx-4 text-lg font-bold">My Locations</h4>
<div class="mx-6">
    <!-- Countries User Can Work In (Get Visa Status) -->
    <h5>Which countries would you like to work in?</h5>
    <div class="mb-4 relative">
        <Search bind:value={countrySearchQuery} placeholder="Search Countries" size="sm"/>
        <Dropdown placement="bottom-start" frameClass="w-full overflow-y-auto max-h-[20rem]" class="w-full">
            {#each locations as location}
                {#if location.name.toLowerCase().includes(countrySearchQuery.toLowerCase())}
                    <DropdownItem defaultClass="p-2 hover:bg-orange-100">
                        {location.name}
                        {@const status = userInfo.job_preferences.location.country_preferences.find(x => x.country_code == location.country_code)?.has_visa}
                        {@const grp = (status === undefined ? "" : status ? "hasvisa" : "novisa")}
                        <Radio class="mx-2" name={location.country_code} group={grp} on:change={updateCountry} value="">No</Radio>
                        <Radio class="mx-2" name={location.country_code} group={grp} on:change={updateCountry} value="hasvisa">Yes</Radio>
                        <Radio class="mx-2" name={location.country_code} group={grp} on:change={updateCountry} value="novisa">Visa Required</Radio>
                    </DropdownItem>
                {/if}
            {/each}
        </Dropdown>
    </div>
    
    <!-- List Of City Preferences -->
    <h5>What cities would you prefer to work in?</h5>
    <div class="mb-4 relative">
        <Search bind:value={citySearchQuery} placeholder="Search Cities" size="sm"/>
        <Dropdown placement="bottom-start" frameClass="w-full overflow-y-auto max-h-[20rem]" class="w-full">
            {#each userInfo.job_preferences.location.country_preferences as {country_code}}
                {#each locations as location}
                    {#if country_code == location.country_code}
                        {#each location.major_cities as city}
                            {#if city.toLowerCase().includes(citySearchQuery.toLowerCase())}
                                <DropdownItem defaultClass="p-2 hover:bg-orange-100">
                                    <Checkbox on:change={(e) => updateCity(e, location.name, city)} checked={userInfo.job_preferences.location.city_preferences.find(x => x.city==city && x.country==location.name) !== undefined}>{country_code}: {city}</Checkbox>
                                </DropdownItem>
                            {/if}
                        {/each}
                    {/if}
                {/each}
            {/each}
        </Dropdown>
    </div>

    <!-- Checkbox (Limit To These Cities Exclusively) -->
    <Checkbox on:change={sendUpdate} bind:checked={userInfo.job_preferences.location.strict_preferences}>Limit searches to these cities? (We will prefer these cities regardless)</Checkbox>
</div>
