import { isJWTValid, getJWT } from '$lib/requestUtils'
import { redirect } from '@sveltejs/kit'
import { page } from '$app/stores'

const publicPaths = ['/login', '/signup']

/** @type { import('./$types').LayoutLoad } */
export function load({ url }) {
	// always allow access to public pages
	if (publicPaths.includes(url.pathname)) {
		return {}
	}

	console.log(getJWT(), isJWTValid())

	if (!isJWTValid()) {
		// console.log('hi')
		// 	throw redirect(301, '/login')
	}

	return {}
}
