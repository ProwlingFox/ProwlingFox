import cookie from 'cookie'
import { browser } from '$app/environment';


const apiUrl = "http://localhost:8000"

function get(path: string) {
	return makeRequest('GET', path)
}

function post(path: string, body: object) {
	return makeRequest('POST', path, body)
}

async function makeRequest(method: string, path: string, body?: object) {
	let headers: Headers = new Headers({
		'Content-Type': 'application/json',
	})

	let JWT = getJWT()
	if (JWT) {
		headers.append('Authorization', 'Bearer ' + JWT)
	}

	let uri = apiUrl + path

	try {
		var response = await fetch(uri, {
			method: method.toUpperCase(),
			body: body ? JSON.stringify(body) : undefined,
			headers: headers,
		})
		return response.json()
	} catch (error) {
		console.error('Fetch Request Failed', error)
		return undefined
	}
}

function getJWT() {
	// Code is different on server vs client
	if (browser) {
		console.log("JWT", "BR")
		let cookies = cookie.parse(document.cookie)
		return cookies.token
	}

	console.log("JWT", "SS")
	return undefined
	
}

function isJWTValid() {
	let JWT = getJWT()
	if (!JWT) {
		return false
	}
	return true
}

async function login(email: string, password: string) {
	const body = {
		email: email,
		password: password,
	}

	const response = await post('/user/login', body)

	if (response.success) {
		document.cookie = `token=${response.Token}; expires=${new Date(
			Date.now() + 1000 * 60 * 60 * 24
		)}; path=/`
		return true
	} else {
		console.warn('Login Error')
		return false
	}
}

export { get, post, login, getJWT, isJWTValid }
