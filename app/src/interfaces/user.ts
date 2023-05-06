// export interface User {
// 	name: string
// 	tel: string
// 	pronouns: string
// 	job_preferences: {
// 		roles: string[]
// 		sector: string
// 		locations: string[]
// 		remote: boolean
// 		salary: number
// 	}
// }

export interface Role{
    role: string
    sector: string
}

export interface City{
    city?: string
    region?: string 
    country: string
}

interface UserDataFields{
    [key: string]: any
    firstname: string
    surname: string
    website: string
    git: string
    linkedIn: string
    phone_number: string
    pronouns: string
    notice_period: string
    expected_sallary: string
    location: string
    address: string
    resume: {
        file_name: string
        data: string
    }
}

interface LocationCriteria{
    can_relocate: boolean
    distance_km: number

    remote_only: boolean
    allowed_countries: string[]
    city_preferences: City[]
    strict_preferences: boolean
}

interface UserJobPreferences{
    roles: Role[]
    location: LocationCriteria
    min_salary: number
}

export interface User {
	name: string
    email: string
    permission: 'admin' | 'candidate' | 'unverified'
	picture?: string

    // Data
    data: UserDataFields
    job_preferences: UserJobPreferences
}
    