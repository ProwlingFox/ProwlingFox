<script lang="ts">
    import type { User } from "$interfaces/user"
    import { PUBLIC_API_URL } from '$env/static/public';
	import { get } from "$lib/requestUtils"
    export let userInfo: User

    let downloader: HTMLAnchorElement;

    async function downloadApplications() {
        const csv = await get("/applications/export")
        console.log(csv)
        const url = URL.createObjectURL(new Blob(
            [csv],
            {type: 'text/csv'}
        ));
        downloader.href = url
        downloader.download = "MyApplications.csv"
        downloader.click()
        setTimeout(() => {
            URL.revokeObjectURL(url)
        }, 2000)
        return url
    }
</script>
<!-- Dummy href for opening file download -->
<a bind:this={downloader} class="hidden" hidden href="#null" >Blank</a>


<div class="p-4">
    <h4 class="my-2 text-lg font-bold">Export My Data</h4>
    <button class="bg-orange-400 p-2 rounded-xl text-white" on:click={downloadApplications}>Export Applications As CSV</button>
</div>

