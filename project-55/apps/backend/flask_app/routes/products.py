from flask import Blueprint, request, jsonify, session
import sys
import json
from flask_app.models import Product
from flask_app.extensions import db

product_bp = Blueprint('products', __name__)


# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)


@product_bp.route('/edit_product', methods=['POST'])
def edit_product():
    try:
        data = request.get_json()
        # print(f"Received data: {data}", file=sys.stderr)

        required_fields = ['id', 'name', 'price', 'description', 'brand', 'options', 'images', 'product_type', 'product_stock']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            print(f"Missing fields: {missing_fields}", file=sys.stderr)
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'message': f"Fields missing: {', '.join(missing_fields)}"
            }), 400

        # Convert id to integer
        product_id = int(data['id'])

        # Locate Product via Product ID
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'success': False,
                'error': 'Product Not Found'
            }), 404

        # Convert stringified options back to a list
        options_str = data['options']
        options_list = json.loads(options_str)  
        cleaned_options = [opt.strip() for opt in options_list] 

        # Convert stringified images back to a list
        images_str = data['images'] 
        images_list = json.loads(images_str)  
        cleaned_images = [img.strip() for img in images_list] 

        # Update product fields
        product.name = data['name']
        product.price = float(data['price'])
        product.description = data['description']
        product.brand = data['brand']
        product.options = cleaned_options  
        product.images = cleaned_images    
        product.product_type = data['product_type']
        product.product_stock = int(data['product_stock'])

        db.session.commit()

        return jsonify({
            'success': True,
            'product_id': product_id
        }), 200

    except json.JSONDecodeError as jde:
        print(f"JSON decode error: {str(jde)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Invalid List Format for Options or Images',
            'message': str(jde)
        }), 400

    except ValueError as ve:
        print(f"ValueError: {str(ve)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Invalid Data Format',
            'message': str(ve)
        }), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error editing product: {str(e)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Failed to Edit Product',
            'message': str(e)
        }), 500


@product_bp.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        # print(f"Received data: {data}", file=sys.stderr)
        required_fields = ['name', 'price', 'description', 'brand', 'options', 'images', 'product_type', 'product_stock']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'message': f"Fields missing: {', '.join(missing_fields)}"
            }), 400
        
        # Convert stringified options back to a list
        options_str = data['options']
        options_list = json.loads(options_str)  
        cleaned_options = [opt.strip() for opt in options_list] 

        # Convert stringified images back to a list
        images_str = data['images'] 
        images_list = json.loads(images_str)  
        cleaned_images = [img.strip() for img in images_list] 

        # Create new Product instance
        new_product = Product(
            name=data['name'],
            price=float(data['price']), 
            description=data['description'],
            brand=data['brand'],
            options=cleaned_options,
            images=cleaned_images,
            product_type=data['product_type'],
            product_stock=int(data['product_stock'])
        )

        # Add to database
        db.session.add(new_product)
        db.session.commit()

        # Update image paths with product_id
        updated_images = [img.replace('product_-1', f'product_{new_product.id}') for img in cleaned_images]
        new_product.images = updated_images
        db.session.commit()

        return jsonify({
            'success': True,
            'product_id': new_product.id
        }), 201

    except ValueError as ve:
        print(f"ValueError: {str(ve)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Invalid Data Format',
            'message': str(ve)
        }), 400

    except Exception as e:
        # Roll back on error and return failure
        db.session.rollback()
        print(f"Error Adding Product: {str(e)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Failed to Add Product',
            'message': str(e)
        }), 500


@product_bp.route('/delete_product', methods=['POST'])
def delete_product():
    try:
        data = request.get_json()
        # print(f"Received data: {data}", file=sys.stderr)

        if 'id' not in data or data['id'] is None:
            return jsonify({
                'success': False,
                'error': 'Product Not Found'
            }), 400

        # Convert id to integer
        product_id = int(data['id'])

        # Locate Product via Product ID
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'success': False,
                'error': 'Product Not Found'
            }), 404

        # Delete Product
        db.session.delete(product)
        db.session.commit()

        return jsonify({
            'success': True,
            'product_id': product_id
        }), 200

    except ValueError as ve:
        print(f"ValueError: {str(ve)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Invalid Product ID Format',
            'message': str(ve)
        }), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting product: {str(e)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Failed to Delete Product',
            'message': str(e)
        }), 500


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
    

@product_bp.route('/get_next_product_id')
def get_next_product_id():
    try:
        # Query the maximum id from the Product table
        max_product = db.session.query(db.func.max(Product.id)).scalar()
        
        # If no products exist, start at 1
        if max_product is None:
            next_id = 1
        else:
            next_id = max_product + 1
        
        return jsonify({
            'success': True,
            'next_id': next_id
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch next product ID',
            'message': str(e)
        }), 500