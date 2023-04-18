import { writable } from 'svelte/store';
import { crossfade as svelteCrossfade } from 'svelte/transition';

const [send, receive] = svelteCrossfade({duration: 400});

interface Application {
    id: string
    companyName: string
    role: string
}

interface ApplicationStore {
    applications: Application[],
    send: any,
    receive: any
}

export const applications = writable<ApplicationStore>({
    applications: [],
    send,
    receive
});