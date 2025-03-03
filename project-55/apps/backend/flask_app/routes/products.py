from flask import Blueprint, jsonify
from flask_app.models import Product

product_bp = Blueprint('products', __name__)


# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)


# add_product route
# goal: add product to product table (dont worry about images right now, just set that to "null")


# remove_product route
# goal: remove product from product table via product id


# get_single_product route
# goal: return a single product via product id


@product_bp.route('/get_all_products')
def get_all_products():
    try:
        products = Product.query.all()
        
        # Check for Missing Data
        if not products:
            return jsonify({
                'success': False,
                'error': 'No products found'
            }), 404
        
        # Serialize the products to a dictionary format for response
        productData = [product.to_dict() for product in products]
        
        # Return Product Data
        return jsonify(productData)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch products',
            'message': str(e)
        }), 500