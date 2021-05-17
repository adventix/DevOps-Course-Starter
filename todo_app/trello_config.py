import os
from dotenv import find_dotenv, load_dotenv
file_path = find_dotenv('.env')
load_dotenv(file_path, override=True)

class Config:

    TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
    if not TRELLO_API_KEY:
        raise ValueError("API Key is not expected value.")
    TRELLO_API_TOKEN = os.environ.get("TRELLO_API_TOKEN")
    if not TRELLO_API_TOKEN:
        raise ValueError("API Token is not expected value.")
