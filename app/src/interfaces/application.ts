import type { Job } from '$interfaces/job'

export enum ApplicationStatus {
    Rejected = -3,
    CandidateRejected = -2,
    Read = -1,
    Unread = 0, // Should Never Occur, Unread applications don't exist as applications
    Requested = 1,
    Processing = 2,
    Processed = 3,
    Reviewed = 4,
    Sending = 5,
    Sent = 6,
    Contact = 7,
    Interviewing = 8,
    Offered = 9,
    Accepted = 10
}

const nullLookup = {
    label: 'Unknown',
    shortLabel: 'Unknown',
    percent: 0,
    color: 'bg-grey-400',
}

// Remember if changing colors here to update the safelist at tailwind.config.js
export const applicationStatusLookup = {
    [ApplicationStatus.Accepted] : nullLookup,
    [ApplicationStatus.Offered] : nullLookup,
    [ApplicationStatus.Interviewing] : nullLookup,
    [ApplicationStatus.Contact] : nullLookup,
    [ApplicationStatus.Sent] : {
        label: 'Application Sent',
        shortLabel: 'Application Sent',
        percent: 100,
        color: 'bg-gray-400',
    },
    [ApplicationStatus.Sending] : {
        label: 'Application Sending',
        shortLabel: 'Application Sending',
        percent: 99,
        color: 'bg-green-400',
    },
    [ApplicationStatus.Reviewed] : {
        label: 'Application Sending',
        shortLabel: 'Application Sending',
        percent: 99,
        color: 'bg-green-400',
    },
    [ApplicationStatus.Processed] : {
        label: 'Application Ready For Review',
        shortLabel: 'Awaiting Review',
        percent: 90,
        color: 'bg-orange-400',
    },
    [ApplicationStatus.Processing] : {
        label: 'Application Processing',
        shortLabel: 'Processing',
        percent: 90,
        color: 'bg-orange-400',
    },
    [ApplicationStatus.Requested] : {
        label: 'Application in Queue',
        shortLabel: 'Pending',
        percent: 33,
        color: 'bg-orange-800',
    },
    [ApplicationStatus.Unread] : nullLookup,
    [ApplicationStatus.Read] : nullLookup,
    [ApplicationStatus.CandidateRejected] : nullLookup,
    [ApplicationStatus.Rejected] : nullLookup,
}
  

export interface Application {
	_id: string
	user_id?: string
	job_id: string
	job: Job
    status: ApplicationStatus

    application_read_ts?: Date
    application_requested_ts?: Date
    application_processing_ts?: Date
    application_processed_ts?: Date
    application_reviewed_ts?: Date
    application_sending_ts?: Date
    application_sent_ts?: Date
    application_contact_ts?: Date
    application_interview_ts?: Date
    application_offer_ts?: Date
    application_accepted_ts?: Date
    application_rejected_ts?: Date
    application_rejected_by_candidate_ts?: Date
	responses?: {
		[key: string]: any;
	}
}

export interface ApplicationStore {
	applications: Application[]
	send: any
	receive: any
}