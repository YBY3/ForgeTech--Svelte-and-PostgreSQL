#connecting model to the database
from flask_app.extensions import db

#Product Model, used the format from frontend provided to create the catalog and order functionalitites
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(550), nullable=False)
    components = db.Column(db.ARRAY(db.String), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    #decided to add a to_dict file to easily convert to a JSON 
    #used to connect to the frontend
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'components': self.components,
            'image': self.image
        }
    
    #user model

#User model
class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(128), nullable=False)
    
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    #decided to add a to_dict file to easily convert to a JSON 
    #used to connect to the frontend
    #removed password to ensure the password is not exposed
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type,
            'profile_pic': self.profile_pic
        }
    
