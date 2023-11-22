from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from .weaviate_schema import create_schema
import weaviate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Initialize Weaviate client and create schema
weaviate_client = weaviate.Client("http://localhost:8080")
create_schema(weaviate_client)

# Import routes after the Flask app has been created and configured
from app import routes