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

#connecting model to the database
from flask_app.extensions import db
from datetime import datetime

#User Model
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

# # Order - Product Relationship Model
# order_product = db.Table(
#     'order_product',
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
# )

#    To do :
    
#     add customizable options such as color, size etc.
#     inform user when they will receive their order (Arrive by)
#     add reviews and stars
#     improve images
#     when image is clicked get more information about the product which will lead to more 
#     images to the lhs and with a long description 
#     frequently bought together section
#     recommend more products to the bottom of the screen

#Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(550), nullable=False)
    brand = db.Column(db.String(64), nullable=False)
    options = db.Column(db.ARRAY(db.String(256)), nullable = True)
    #for multiple images 
    images = db.Column(db.ARRAY(db.String(256)), nullable = False)
    #product type e.b GPU, CPU, RAM...
    product_type = db.Column(db.String(50), nullable = False)
    #product_stock 
    product_stock = db.Column(db.Integer, nullable = False, default = 100000)
    
# Establishes a relationship between Product and OrderProduct tables.
# This allows each Product to be linked to multiple orders via the OrderProduct table.
# 
#  `orders = db.relationship('OrderProduct', back_populates='product')`:
#   - The `orders` attribute in the Product model references the OrderProduct table.
#   - The `back_populates='product'` ensures that OrderProduct also has a `product` reference, 
#     allowing bidirectional access.
# 
#  Why use `db.relationship` instead of just ForeignKey?
#   - We need a **many-to-many relationship** between Product and Order.
#   - Instead of using a simple association table (`db.Table`), we use `OrderProduct` as a full model 
#     because it stores extra attributes like `order_quantity`.
#   - This avoids manually querying OrderProduct when retrieving orders for a product.
#
#  How to use this relationship:
#   - `product.orders` → Gives all OrderProduct records linked to this Product.
#   - `order_product.product` → Gives the Product associated with an OrderProduct record.
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
            'images': self.images,
            'product_type': self.product_type,
            'product_stock': self.product_stock,
            'options': self.options        }


# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Link the order to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relationship with Products
    # products = db.relationship('Product', secondary=order_product, back_populates='orders')
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    # Link to employee
    claimed_by_employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  
    # Timestamp for ordering
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    arrive_by = db.Column(db.DateTime, default=datetime.utcnow) 

 
    #relationship with OrderProduct
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
            # To show claim status
            'claimed_by_employee_id': self.claimed_by_employee_id,  
             # To show creation timestamp
            'created_at': self.created_at,
            'arrive_by': self.arrive_by
        }
    
#created a OrderProduct Model 
class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #order table is linked to the order table
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable = False)
    #product_id is linked to the product table
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    #tracks quanity of order
    order_quantity = db.Column(db.Integer, nullable = False, default = 1)


  # Relationships to Order and Product
    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='orders')

    def __repr__(self):
        return f'<OrderProduct OrderID: {self.order_id}, ProductID: {self.product_id}>'

    
