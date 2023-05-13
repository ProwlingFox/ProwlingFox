import { invaldateUserData, userData } from '$lib/userData.js'
import { get as getStore } from 'svelte/store'

export async function load() {
	if(!getStore(userData)) {
		await invaldateUserData()
	}

	return
}
