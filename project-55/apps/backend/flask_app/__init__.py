from flask import Flask
from flask_cors import CORS
from flask_app.extensions import db
from flask_app.routes import main
from flask_app.models import User

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    db.init_app(app)
    app.register_blueprint(main)
    CORS(app)
    return app