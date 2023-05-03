import type { Job } from '$interfaces/job'

export interface Application {
	_id: string
	user_id?: string
	job_id: string
	job: Job
	application_read: boolean
	application_requested: boolean
	application_processing: boolean
	application_processed: boolean
    application_reviewed: boolean
    application_sending: boolean
    application_sent: boolean
	progress: ApplicationStatus
	responses: {
		[key: string]: any;
	}
}

export interface ApplicationStore {
	applications: Application[]
	send: any
	receive: any
}

export interface ApplicationStatus {
	label: string
	percent: number
	color: string
}
