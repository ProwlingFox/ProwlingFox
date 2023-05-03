<script lang="ts">
    import ApplicationSwitcher from '$components/ApplicationSwitcher.svelte'
</script>

<ApplicationSwitcher selectedTab="Current Role">
    <div class="flex w-full justify-center overflow-auto">
        <slot />
    </div>
</ApplicationSwitcher> 