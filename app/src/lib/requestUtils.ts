import cookie from 'cookie'
import { browser } from '$app/environment'
import { readable, get as getStore } from 'svelte/store'
import type { Readable } from 'svelte/store'
import jwt_decode from 'jwt-decode'
import { PUBLIC_API_URL } from '$env/static/public';

const apiUrl = PUBLIC_API_URL
let JWTStore: Readable<string>

function get(path: string, fetch_override: Function = fetch, params: {[key: string]: string | number | boolean} = {}) {
	return makeRequest('GET', path, undefined, params=params, fetch_override)
}

function post(path: string, body: object, fetch_override: Function = fetch, params: {[key: string]: string | number | boolean} = {}) {
	return makeRequest('POST', path, body, params, fetch_override )
}

async function makeRequest(method: string, path: string, body: object = {}, params: {[key: string]: string | number | boolean} = {}, fetch_override: Function = fetch) {
	let headers: Headers = new Headers({
		'Content-Type': 'application/json',
	})

	let JWT = getJWT()
	if (JWT) {
		headers.append('Authorization', 'Bearer ' + JWT)
	}

	let uri = apiUrl + path

	if (params) {
		const stringified_params: {[key: string]: string} = {}
		for (const key in params) {
			stringified_params[key] = params[key].toString()
		}
		uri += "?" + new URLSearchParams(stringified_params).toString()
	}

	try {
		let fetch_obj: RequestInit = {
			method: method.toUpperCase(),
			headers: headers,
		}
		if (method == "POST") {fetch_obj["body"] = JSON.stringify(body)}

		var response = await fetch_override(uri, fetch_obj)
		if (response.ok) {
			const contentType: string = response.clone().headers.get("content-type")
			if (contentType.includes("text/csv")) return response.text()
			return response.json()
		} 
		throw response
	} catch (error) {
		console.error('Fetch Request Failed', error)
		return {}
	} 
}

function setJWT(JWT: string) {
	// For Setting The JWT
	if (browser) {
		//Don't Set On Browser
		return null
	}

	JWTStore = readable(JWT)
}

function getJWT() {
	// Code is different on server vs client
	if (browser) {
		let cookies = cookie.parse(document.cookie)
		return cookies.token
	} else {
		return getStore(JWTStore)
	}
}

interface DecodedJWT {
	expiry: number
	permission: string
	user_id: string
	name: string
	email: string
	profileImage: string
	linkedInAccessKey: string
}

function parseJWT(): DecodedJWT | null {
	let JWT = getJWT()
	if (!JWT) {
		return null
	}
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

async function loginLinkedIn(code: string) {
	const body = {
		code: code
	}

	const response = await post('/user/login/linkedin', body)

	if (response.success) {
		if(browser){
			document.cookie = `token=${response.Token}; expires=${new Date(
				Date.now() + 1000 * 60 * 60 * 24 * 30
			)}; path=/`
			return true
		}
		return false
	} else {
		console.warn('Login Error')
		return false
	}
}

export { get, post, login, loginLinkedIn, getJWT, setJWT, parseJWT, isJWTValid }
