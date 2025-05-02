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

    # Relationships
    threads = db.relationship('Thread', back_populates='creator', lazy='dynamic')
    messages = db.relationship('Message', back_populates='user', lazy='dynamic')

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
    hidden = db.Column(db.Boolean, default=False)

    # Relationships
    image_ids = db.relationship('ImageProduct', back_populates='product')
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
            'image_ids': [image_product.image.id for image_product in self.image_ids],
            'product_type': self.product_type,
            'product_stock': self.product_stock,
            'options': self.options,
            'hidden': self.hidden
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
    hidden = db.Column(db.Boolean, default=False)

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
            'arrive_by': self.arrive_by.isoformat(),
            'hidden': self.hidden
        }
    

# Image Model
class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Image {self.name}>'
    

# Message Model
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    responding_to_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=True)
    message = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    thread = db.relationship('Thread', back_populates='messages')
    user = db.relationship('User', back_populates='messages')
    replies = db.relationship('Message', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def __repr__(self):
        return f'<id: {self.id}, thread_id: {self.thread_id}, user_id: {self.user_id}, responding_to_id: {self.responding_to_id}, message: {self.message[:20]}>'
    

# Thread Model
class Thread(db.Model):
    __tablename__ = 'thread'
    id = db.Column(db.Integer, primary_key=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    creator = db.relationship('User', back_populates='threads')
    messages = db.relationship('Message', back_populates='thread', lazy='dynamic')

    def __repr__(self):
        return f'<Thread ID: {self.id}, Name: {self.name}>'

    
# Order Product Relationship
class OrderProduct(db.Model):
    __tablename__ = 'order_product'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_quantity = db.Column(db.Integer, nullable=False, default=1)
    product_option = db.Column(db.String(256), nullable=True)

    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='orders')

    def __repr__(self):
        return f'<OrderProduct OrderID: {self.order_id}, ProductID: {self.product_id}>'
    

# Image Product Relationship
class ImageProduct(db.Model):
    __tablename__ = 'image_product'
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

    image = db.relationship('Image', backref='image_products')
    product = db.relationship('Product', back_populates='image_ids')

    def __repr__(self):
        return f'<ImageProduct ImageID: {self.image_id}, ProductID: {self.product_id}>'