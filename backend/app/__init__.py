from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

import  os


def create_app():
    load_dotenv(find_dotenv(), override=True)

    site_sense_app: Flask = Flask(__name__)
    site_sense_app.config.from_object("app.config")  # Load the config file

    # Enable CORS so the frontend cna call the backend from a different origin
    ORIGIN = os.getenv("ORIGIN")
    ENDPOINT = os.getenv("ENDPOINT")
    CORS(app=site_sense_app,
         resources={f"/{ENDPOINT}": {"origins": ORIGIN}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"])

    # Import and register your routes as a Blueprint
    from .routes import bp
    site_sense_app.register_blueprint(bp)
    
    return site_sense_app
