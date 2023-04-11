export function handleEnterKey(e: KeyboardEvent, callback: Function): void {
	if (e.key === 'Enter') {
		callback()
	}
}
