export interface Job {
	id: string
	source: string
	ext_ID: string
	added_ts: number
	last_updated_ts: number
	created_ts: number
	raw_data?: any
	long_description: any
	role: string
	company: {
		name: string
		logo?: string
		website?: string
		tagline?: string
		employee_count?: any
		sectors?: string[]
	}
	short_description: string
	location: string
	salary?: string
	salary_currency?: any
	remote?: any
	role_category: string
	skills: string[]
	status: 'Active' | 'Inactive'
}
