from flask import Blueprint
from .extensions import db
from .models import Product

main = Blueprint('main', __name__)

#Provides Product Data
@main.route('/products')
def get_products():
    products = Product.query.all()
    productData = [product.to_dict() for product in products]
    return productData