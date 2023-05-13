import { writable, get as getStore } from 'svelte/store'
import { get, post } from './requestUtils'
import type { User } from '$interfaces/user'

export const userData = writable<User>(
    // await get("/user")
)

export async function invaldateUserData() {
    userData.set(await get("/user"))
}

export async function saveUserData() {
    post('/user/update', getStore(userData))
}