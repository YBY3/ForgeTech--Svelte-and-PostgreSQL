from flask_app.extensions import db
from flask_app.models import Product
from flask_app import create_app

app = create_app()

with app.app_context():
    products = [
        Product(
            name="Sample GPU",
            price=9.99,
            description="Graphics Processing Unit",
            components=["Color", "Make", "Year"],
            image="/catalog-images/gpu.jpg"
        ),
        Product(
            name="Sample CPU",
            price=12.49,
            description="Central Processing Unit",
            components=["Color", "Make", "Year"],
            image="/catalog-images/cpu.jpg"
        ),
        Product(
            name="Sample Keyboard",
            price=8.99,
            description="Wireless Bluetooth Keyboard",
            components=["Color", "Make", "Year"],
            image="/catalog-images/keyboard.jpg"
        ),
        Product(
            name="Sample Monitor",
            price=149.99,
            description="27-inch LED Monitor",
            components=["Resolution", "Size", "Refresh Rate"],
            image="/catalog-images/monitor.jpg"
        )
    ]

    db.session.add_all(products)
    db.session.commit()

