import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN")
IMAGE_FOLDER = 'images'

#Buttons for bot
HISTORY = 'History of searches'
SEARCH = 'Search for an item'
OZON = 'Озон'
MVIDEO = 'МВидео'
WB = 'Wildberries'
ALL = 'Search in all'