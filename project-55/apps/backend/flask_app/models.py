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
   
    def __repr__(self):
        return f'<User {self.name}>'
   
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type,
            'profile_pic': self.profile_pic
        }




# Order - Product Relationship Model
order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)




#Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(550), nullable=False)
    components = db.Column(db.ARRAY(db.String), nullable=False)
    image = db.Column(db.String(120), nullable=False)
   
    orders = db.relationship('Order', secondary=order_product, back_populates='products')
   
    def __repr__(self):
        return f'<Product {self.name}>'
   
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'components': self.components,
            'image': self.image
        }




# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Link the order to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relationship with Products
    products = db.relationship('Product', secondary=order_product, back_populates='orders')
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    # Link to employee
    claimed_by_employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  
    # Timestamp for ordering
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  


    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_ids': [product.id for product in self.products],
            'total': self.total,
            'status': self.status,
            # To show claim status
            'claimed_by_employee_id': self.claimed_by_employee_id,  
             # To show creation timestamp
            'created_at': self.created_at
        }

