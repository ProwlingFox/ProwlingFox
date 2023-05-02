import { isJWTValid, setJWT, getJWT, parseJWT} from '$lib/requestUtils'
import { redirect } from '@sveltejs/kit'

const publicPaths = ['/login', '/signup']


/** @type {import('./$types').LayoutLoad} */
export async function load({ url, params }) {
	if (isJWTValid()) {
		if (parseJWT()?.permission == "unverified" && url.pathname != "/invite") {
			throw redirect(301, '/invite')
		}
		if (publicPaths.includes(url.pathname)) {
			throw redirect(301, '/')
		}
		return {
			authenticated: true
		}
	}

	// // always allow access to public pages
	if (publicPaths.includes(url.pathname)) {
		return {
			authenticated: false
		}
	}

	throw redirect(301, '/login')
}