from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from .weaviate_services import initialize_weaviate_client

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Initialize Weaviate client
app.weaviate_client = initialize_weaviate_client(app.config['WEAVIATE_URL'])

# Import routes after the Flask app has been created and configured
from app import routes