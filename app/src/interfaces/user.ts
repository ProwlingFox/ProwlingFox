export interface User {
	name: string
	tel: string
	pronouns: string
	job_preferences: {
		roles: string[]
		sector: string
		locations: string[]
		remote: boolean
		salary: number
	}
}
