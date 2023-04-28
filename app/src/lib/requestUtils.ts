import cookie from 'cookie'
import { browser } from '$app/environment'
import { readable, get as getStore } from 'svelte/store'
import type { Readable } from 'svelte/store'
import jwt_decode from "jwt-decode";

const apiUrl = "http://localhost:8000"
let JWTStore: Readable<string>;

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
		if (response.ok)
			return response.json()
		else 
			throw response
	} catch (error) {
		console.error('Fetch Request Failed', error)
		return {}
	}
}

function setJWT(JWT: string) {
	// For Setting The JWT
	if (browser) {	//Don't Set On Browser
		return null;
	}

	JWTStore = readable(JWT)

}

function getJWT() {
	// Code is different on server vs client
	if (browser){
		let cookies = cookie.parse(document.cookie)
		return cookies.token
	} else {
		return getStore(JWTStore)
	}
}

interface DecodedJWT {
	expiry: number,
	permission: string,
	user_id: string,
	name: string,
	email: string
}

function parseJWT(): DecodedJWT | null {
	let JWT = getJWT()
	if (!JWT) { return null }
	var decoded = jwt_decode<DecodedJWT>(JWT)
	return decoded
}

function isJWTValid(): Boolean {
	let JWT = parseJWT()

	if (!JWT) return false
	if (new Date(JWT.expiry * 1000) < new Date()) return false

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

export { get, post, login, getJWT, setJWT, parseJWT, isJWTValid }
