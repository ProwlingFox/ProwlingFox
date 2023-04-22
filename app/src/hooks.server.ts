import { setJWT } from '$lib/requestUtils';
import { parse } from 'cookie';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {

    const { headers } = event.request;
    const cookies = parse(headers.get("Cookie") ?? "");

    setJWT(cookies?.token)

    const response = await resolve(event);

    return response;
}