<script lang="ts">
    import type { User } from "$interfaces/user"
    import { PUBLIC_API_URL } from '$env/static/public';
	import { get } from "$lib/requestUtils"
    export let userInfo: User

    let downloader: HTMLAnchorElement;

    async function downloadApplications() {
        const csv = await get("/user/data/applications")
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

Settings

<button on:click={downloadApplications}>Export Applications As CSV</button>
<a bind:this={downloader} class="hidden" hidden href="#null" >Blank</a>