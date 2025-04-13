"""
Database Models Documentation

This module defines the database models for a Flask application, including Users, Products, Orders, and OrderProduct. 
It establishes relationships between entities using SQLAlchemy ORM.

### Models Overview:
- **User Model**: Stores user account information.
- **Product Model**: Stores product details, including inventory tracking.
- **Order Model**: Stores order details and links to users.
- **OrderProduct Model**: Acts as a junction table between Order and Product to manage order items and quantities.

Objectives:
- Track product inventory and categorize products using `product_inventory` and `product_type`.
- Enhance product visualization with multiple images using `images`.
- Establish bidirectional relationships between tables using SQLAlchemy relationships and foreign keys.
"""

from flask_app.extensions import db
from datetime import datetime


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=True)
    profile_pic = db.Column(db.String(128), nullable=True)
    user_type = db.Column(db.String(128), nullable=False)
    registered_by = db.Column(db.DateTime, default=datetime.utcnow)
    active_by = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'
   
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type,
            'profile_pic': self.profile_pic,
            'registered_by': self.registered_by,
            'active_by': self.active_by
        }
    

# Product Model
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(550), nullable=False)
    brand = db.Column(db.String(64), nullable=False)
    options = db.Column(db.ARRAY(db.String(256)), nullable=True)
    product_type = db.Column(db.String(50), nullable=False)
    product_stock = db.Column(db.Integer, nullable=False, default=100000)

    images = db.relationship('ImgProduct', back_populates='product')
    orders = db.relationship('OrderProduct', back_populates='product')

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'brand': self.brand,
            'images': [img_product.img.id for img_product in self.images],
            'product_type': self.product_type,
            'product_stock': self.product_stock,
            'options': self.options
        }


# Order Model
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    claimed_by_employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    arrive_by = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship('OrderProduct', back_populates='order')

    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_ids': [item.product_id for item in self.order_items],
            'total': self.total,
            'status': self.status,
            'claimed_by_employee_id': self.claimed_by_employee_id,
            'created_at': self.created_at.isoformat(),
            'arrive_by': self.arrive_by.isoformat()
        }
    

# Img Model
class Img(db.Model):
    __tablename__ = 'img'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Img {self.name}>'

    
# Order Product Relationship
class OrderProduct(db.Model):
    __tablename__ = 'order_product'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_quantity = db.Column(db.Integer, nullable=False, default=1)

    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='orders')

    def __repr__(self):
        return f'<OrderProduct OrderID: {self.order_id}, ProductID: {self.product_id}>'
    

# Img Product Relationship
class ImgProduct(db.Model):
    __tablename__ = 'img_product'
    img_id = db.Column(db.Integer, db.ForeignKey('img.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

    img = db.relationship('Img', backref='img_products')
    product = db.relationship('Product', back_populates='images')

    def __repr__(self):
        return f'<ImgProduct ImgID: {self.img_id}, ProductID: {self.product_id}>'
