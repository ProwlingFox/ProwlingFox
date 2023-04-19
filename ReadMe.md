# Prowling Fox

A GPT3 App to automate job applications. Now with an Interface!

## Getting Started

### Starting Mongo

1. Install Docker
2. Run Docker Compose Up In The Project Directory

### Setup ENV Vars

1. Copy `/api/secrets.json.example` to `/api/secrets.json`
2. Edit `/api/secrets.json` with the correct details.

### Populating The DB With Jobs

1. Create a Py Env with `python3 -m venv env` then activate
2. Run `pip install -r requirements.txt` to install dependancies
3. Run `siteScraperService.py` Until enough jobs are inserted into the DB for your usecase

### Starting The API Service

1. Run `uvicorn api:app --reload`
2. Navigate to `localhost:8000/docs` to view the API Docs
