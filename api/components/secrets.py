import json

secrets = None;

def init():
	#Load Secrets
	fSecrets = open("secrets.json", "r")
	global secrets;
	secrets = json.load(fSecrets)
	fSecrets.close()