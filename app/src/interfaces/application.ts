import type { Job } from '$interfaces/job'

enum ApplicationState {
    Read = -1,
    Unread = 0, // Should Never Occur, Unread applications don't exist as applications
    Requested = 1,
    Processing = 2,
    Processed = 3,
    Reviewed = 4,
    Sending = 5,
    Sent = 5,
    Contact = 6,
    Interviewing = 7,
    Offered = 8,
    Accepted = 9
}
  

export interface Application {
	_id: string
	user_id?: string
	job_id: string
	job: Job
    state: ApplicationState

	application_read: boolean
    application_read_ts: Date
    application_requested: boolean
    application_requested_ts: Date
    application_processing: boolean
    application_processing_ts: Date
    application_processed: boolean
    application_processed_ts: Date
    application_reviewed: boolean
    application_reviewed_ts: Date
    application_sending: boolean
    application_sending_ts: Date
    application_sent: boolean
    application_sent_ts: Date
    application_contact: boolean
    application_contact_ts: Date
    application_interview: boolean
    application_interview_ts: Date
    application_offer: boolean
    application_offer_ts: Date
    application_accepted: boolean
    application_accepted_ts: Date
    application_rejected: boolean
    application_rejected_ts: Date
    application_rejected_by_candidate: boolean
    application_rejected_by_candidate_ts: Date
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
