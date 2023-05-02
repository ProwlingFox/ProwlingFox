
/** @type {import('./$types').PageLoad} */
export function load({ url }) {
    let code = url.searchParams.get("code")

	return {
        code: code
    }
}
