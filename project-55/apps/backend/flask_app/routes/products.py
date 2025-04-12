from flask import Blueprint, request, jsonify
import sys, json, base64
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
from flask_app.models import Product, Img, ImgProduct, OrderProduct
from flask_app.extensions import db


# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)


product_bp = Blueprint('products', __name__)


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

        required_fields = ['name', 'price', 'description', 'brand', 'options', 'product_type', 'product_stock']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': 'Missing Product Info',
                'message': f"Fields missing: {', '.join(missing_fields)}"
            }), 400
        
        # Convert stringified options back to a list
        options_str = data['options']
        options_list = json.loads(options_str)  
        cleaned_options = [opt.strip() for opt in options_list] 

        # Handle Files (base64 images)
        files = data.get('files', [])
        image_ids = []
        for file_data in files:
            try:
                # Decode base64 image
                img_data = base64.b64decode(file_data['data'])
                img = Img(
                    img=img_data,
                    mimetype=file_data['type'],
                    name=file_data['name']
                )
                db.session.add(img)
                db.session.flush()
                image_ids.append(img.id)
            except (KeyError, ValueError) as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'error': 'Invalid image data',
                    'message': f"Image processing failed: {str(e)}"
                }), 400

        # Create new Product instance
        new_product = Product(
            name=data['name'],
            price=float(data['price']), 
            description=data['description'],
            brand=data['brand'],
            options=cleaned_options,
            product_type=data['product_type'],
            product_stock=int(data['product_stock'])
        )

        # Add to database
        db.session.add(new_product)
        db.session.commit()

        # Link images via ImgProduct
        for img_id in image_ids:
            img_product = ImgProduct(
                img_id=img_id,
                product_id=new_product.id
            )
            db.session.add(img_product)

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
        
        # Get associated ImgProduct records
        img_products = ImgProduct.query.filter_by(product_id=product_id).all()
        img_ids = [ip.img_id for ip in img_products]

        # Delete ImgProduct records
        for img_product in img_products:
            db.session.delete(img_product)

        # Delete Linked Img records
        for img_id in img_ids:
            other_links = ImgProduct.query.filter_by(img_id=img_id).count()
            if other_links == 0:
                img = Img.query.get(img_id)
                if img:
                    db.session.delete(img)
        
        # Delete associated OrderProduct records
        OrderProduct.query.filter_by(product_id=product_id).delete()

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


@product_bp.route('/get_all_products', methods=['GET'])
def get_all_products():
    try:
        # Eagerly load ImgProduct and Img
        products = Product.query.options(
            joinedload(Product.images).joinedload(ImgProduct.img)
        ).all()
        
        # Check for Missing Data
        if not products:
            return jsonify({
                'success': True,
                'data': []
            }), 200
        
        # Serialize products
        productData = [product.to_dict() for product in products]
        
        return jsonify({
            'success': True,
            'data': productData
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to Fetch Products',
            'message': str(e)
        }), 500