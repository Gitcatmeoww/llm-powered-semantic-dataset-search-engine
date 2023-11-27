import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEAVIATE_URL = os.getenv('WEAVIATE_URL')
    OPENAI_APIKEY = os.getenv('OPENAI_APIKEY')
