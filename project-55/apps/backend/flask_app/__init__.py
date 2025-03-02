from flask import Flask
from datetime import timedelta
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_app.extensions import db
from flask_app.routes import main

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY')
    app.config.from_prefixed_env()
    db.init_app(app)
    app.register_blueprint(main)
    CORS(app)
    return app