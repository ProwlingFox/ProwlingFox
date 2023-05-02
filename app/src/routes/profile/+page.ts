import type { User } from '$interfaces/user.js'
import { get } from '$lib/requestUtils.js'

/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch }) {
	const userInfo: User = await get("/user", fetch)
	return {
		userInfo: userInfo
	}
}
