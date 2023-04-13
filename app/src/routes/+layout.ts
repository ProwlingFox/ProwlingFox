import { isJWTValid, setJWT, getJWT} from '$lib/requestUtils'
import { redirect } from '@sveltejs/kit'

const publicPaths = ['/login', '/signup']


/** @type {import('./$types').LayoutServerLoad} */
export function load({ url, data }) {
	setJWT(data.token)

	// always allow access to public pages
	if (publicPaths.includes(url.pathname)) {
		return {}
	}

	if (!isJWTValid()) {
		throw redirect(301, '/login')
	}

	return {
		// JWT: JWT
	}
}