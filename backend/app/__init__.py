from flask import Flask
from flask_cors import CORS

def create_app():
    site_sense_app: Flask = Flask(__name__)
    site_sense_app.config.from_object("app.config")  # Load the config file

    CORS(site_sense_app)  # Enable CORS so the frontend cna call the backend from a different origin

    # Import and register your routes as a Blueprint
    from .routes import bp
    site_sense_app.register_blueprint(bp)
    
    return site_sense_app
