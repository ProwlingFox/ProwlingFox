import json

def init():
	#Load Secrets
	fSecrets = open("secrets.json", "r")
	secrets = json.load(fSecrets)
	fSecrets.close()
	return secrets

secrets = init()