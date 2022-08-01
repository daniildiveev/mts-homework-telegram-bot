import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

TOKEN = os.environ.get("TOKEN")

#Buttons for bot
HISTORY = 'History of searches'
SEARCH = 'Search for an item'
MVIDEO = 'МВидео'
TEKNOPARK = 'Технопарк'
ALL = 'Search in all'
MAX_REQUESTS_TO_SHOW = 10

#Database settings
class Settings(BaseModel):
    database_source: str = 'sqlite:///./sql_app.db'

settings = Settings()