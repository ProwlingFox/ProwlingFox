import cookie from 'cookie'

function get(uri: string) {
	return makeRequest('GET', uri)
}

function post(uri: string, body: object) {
	return makeRequest('POST', uri, body)
}

async function makeRequest(method: string, uri: string, body?: object) {
	let headers: Headers = new Headers({
		"Content-Type": "application/json",
	 });


	let JWT = getJWT()
	if (JWT) {
		headers.append('Authorization', 'Bearer ' + JWT)
	}

	try {
		var response = await fetch(uri, {
			method: method.toUpperCase(),
			body: body ? JSON.stringify(body) : undefined,
			headers: headers
		})
		return response.json()
	} catch(error) {
		console.error("Fetch Request Failed", error)
		return undefined;
	}


}

function getJWT() {
	if(typeof document == 'undefined') {
		return undefined
	}

	let cookies = cookie.parse(document.cookie)
	return cookies.token
}

function isJWTValid() {
	let JWT = getJWT();
	if (! JWT) {
		return false
	}
	return true
}

async function login(email: string, password: string) {
	const body = {
		"email": email,
		"password": password
	}

	const response = await post('http://localhost:8000/user/login', body)

	if(response.success) {
		document.cookie = `token=${response.Token}; expires=${(new Date(Date.now() + 1000 * 60 * 60 * 24))}; path=/`
		return true
	} else {
		console.warn("Login Error")
		return false
	}

}

export {
	get,
	post,
	login,
	isJWTValid
}