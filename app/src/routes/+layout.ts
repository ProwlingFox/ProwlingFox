import { isJWTValid, setJWT, getJWT} from '$lib/requestUtils'
import { redirect } from '@sveltejs/kit'

const publicPaths = ['/login', '/signup']


/** @type {import('./$types').LayoutLoad} */
export async function load({ url, params }) {
	if (isJWTValid()) {
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