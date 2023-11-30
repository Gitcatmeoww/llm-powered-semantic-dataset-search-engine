from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
import weaviate


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Initialize Weaviate client
weaviate_client = weaviate.Client(
    url=app.config['WEAVIATE_URL'],
    additional_headers={
        "X-OpenAI-Api-Key": app.config["OPENAI_APIKEY"]
    }
)

# Load NLP model
# nlp_model = pipeline("feature-extraction", model="bert-base-uncased")

# Import routes and schema creation after the Flask app has been created
from .weaviate_schema import create_schema
create_schema(weaviate_client)

from app import routes

# app.nlp_model = nlp_model