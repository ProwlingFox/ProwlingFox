# Interfaces

## Job
Defines attributes to do with jobs

inteface job {
    <!-- Technical Interfaces -->
    jobID: String - Primary ID of Job
    jobSource: String - Unique Source of Job i.e. workable, related to plugin
    jobExtID: String - ID of job in Source 
}



Job Scraping Plugin interface

__init__ 

Will Accept a Dict Input from 
Iter that returns 