import cookie from 'cookie'

function get(uri) {
	return makeRequest('GET', uri)
}

function post(uri, body) {
	return makeRequest('POST', uri, body)
}

async function makeRequest(method, uri, body) {
	let headers = {
		'content-type': 'application/json'
	}

	let JWT = getJWT()
	if (JWT) {
		headers['Authorization'] = 'Bearer ' + JWT
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

async function login(email, password) {
	const body = {
		"email": email,
		"password": password
	}

	const response = await post('http://localhost:8000/user/login', body)

	if(response) {
		document.cookie = `token=${response.Token}; expires=${(new Date(Date.now() + 1000 * 60 * 60 * 24))}; path=/`
	} else {
		alert("Login Error")
	}
}

export {
	get,
	post,
	login
}