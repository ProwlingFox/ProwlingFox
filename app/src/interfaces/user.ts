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

export interface UserFile{
    file_name: string
    data: string
}

// Maybe Theres a way to deal w/ this but honestly it never shoulda been hardcoded
interface UserDataFields{
    [key: string]: {
        [key: string] : any
        Text?: string
        Number?: number
        Checkbox?: Boolean
        Date?: Date
        File?: UserFile
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
    _id: string
	name: string
    email: string
    permission: 'admin' | 'candidate' | 'unverified'
	picture?: string

    // Data
    data: UserDataFields
    job_preferences: UserJobPreferences
}
    
export interface UserStats {
    applicationsToday: number
}