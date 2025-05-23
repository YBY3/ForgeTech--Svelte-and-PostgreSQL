from flask import Flask
import os
from flask_cors import CORS
from flask_app.extensions import db
from flask_app.routes.users import user_bp;
from flask_app.routes.products import product_bp;
from flask_app.routes.orders import order_bp;
from flask_app.routes.ordersControl import order_control_bp;
from flask_app.routes.images import image_bp;
from flask_app.routes.threads import thread_bp;


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY')
    app.config.from_prefixed_env()
    db.init_app(app)


    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(order_control_bp, url_prefix='/api/ordersControl')
    app.register_blueprint(image_bp, url_prefix='/api/images')
    app.register_blueprint(thread_bp, url_prefix='/api/threads')
    CORS(app)
    return app