<script lang="ts">
    import ApplicationSwitcher from '$components/ApplicationSwitcher.svelte'
</script>

<ApplicationSwitcher>
    <div class="flex w-full justify-center overflow-auto">
        <slot />
    </div>
</ApplicationSwitcher> 