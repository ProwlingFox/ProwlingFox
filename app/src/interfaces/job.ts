export interface Job {
	_id: string
	source: string
	ext_ID: string
	added_ts: number
	last_updated_ts: number
	created_ts: number
	raw_data?: any
	long_description: any
	role: string
	role_description: string
	requirements: string[]
	key_points: string[]
	company: {
		name: string
		short_description?: string
		logo?: string
		website?: string
		tagline?: string
		employee_count?: any
		sectors?: string[]
	}
	short_description: string
	location: {
		city: string
		region?: string
		country: string
	}
	salary?: string
	salary_currency?: any
	remote?: any
	role_category: string[]
	skills: string[]
	status: 'Active' | 'Inactive'
	questions: Question[]
}

interface Question {
	id: string
    content: string
    type: string
    required: boolean
    choices?: Choice[]
    response?: any
}

interface Choice{
	id: string
    content: string
    raw_data?: any
}
    