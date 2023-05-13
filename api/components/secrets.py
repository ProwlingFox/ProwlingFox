from dotenv import load_dotenv
import os

def init():
	load_dotenv()
	return os.environ

secrets = init()