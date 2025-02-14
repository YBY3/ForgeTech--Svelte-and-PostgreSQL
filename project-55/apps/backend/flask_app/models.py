#connecting model to the database
from flask_app.extensions import db

# Example User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
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