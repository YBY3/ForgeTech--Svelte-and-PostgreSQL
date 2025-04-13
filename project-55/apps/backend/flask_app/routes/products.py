from flask import Blueprint, request, jsonify
import sys, json, base64
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
from flask_app.models import Product, Image, ImageProduct, OrderProduct
from flask_app.extensions import db


# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)


product_bp = Blueprint('products', __name__)
ALLOWED_MIMETYPES = {'image/jpeg', 'image/png', 'image/gif'}


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

        # Handle Images (base64 images)
        files = data.get('files', [])
        image_ids = []
        max_image_size = 10 * 1024 * 1024  # 10MB in bytes

        if len(files) > 5:
            return jsonify({
                'success': False,
                'error': 'More Than 5 Images Found'
            }), 400

        for file_data in files:
            try:
                # Check MIME type
                if file_data['type'] not in ALLOWED_MIMETYPES:
                    db.session.rollback()
                    return jsonify({
                        'success': False,
                        'error': 'Invalid Image Type Found',
                        'message': f"Image '{file_data['name']}' has unsupported type '{file_data['type']}'. Allowed types: {', '.join(ALLOWED_MIMETYPES)}"
                    }), 400

                # Decode base64 image
                image_data = base64.b64decode(file_data['data'])

                # Check image size
                if len(image_data) > max_image_size:
                    db.session.rollback()
                    return jsonify({
                        'success': False,
                        'error': 'Large Image Found (Exceeds 10MB)',
                        'message': f"Image '{file_data['name']}' Exceeds 10MB limit"
                    }), 400

                # Create New Image Instance
                image = Image(
                    image=image_data,
                    mimetype=file_data['type'],
                    name=file_data['name']
                )
                db.session.add(image)
                db.session.flush()
                image_ids.append(image.id)
            except (KeyError, ValueError) as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'error': 'Invalid Image Data',
                    'message': f"Image Processing Failed: {str(e)}"
                }), 400

        # Create New Product Instance
        product = Product(
            name=data['name'],
            price=float(data['price']), 
            description=data['description'],
            brand=data['brand'],
            options=cleaned_options,
            product_type=data['product_type'],
            product_stock=int(data['product_stock'])
        )

        # Add to Database
        db.session.add(product)
        db.session.commit()

        # Link Images via ImageProduct Relationship
        for image_id in image_ids:
            # Create New ImageProduct Instance
            image_product = ImageProduct(
                image_id=image_id,
                product_id=product.id
            )
            db.session.add(image_product)

        #Commit Changes
        db.session.commit()

        return jsonify({
            'success': True
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

        # Convert ID to Integer
        product_id = int(data['id'])

        # Locate Product via Product ID
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'success': False,
                'error': 'Product Not Found'
            }), 404
        
        # Get Associated ImageProduct Records
        image_products = ImageProduct.query.filter_by(product_id=product_id).all()
        image_ids = [image_product.image_id for image_product in image_products]

        # Delete ImageProduct Records
        for image_product in image_products:
            db.session.delete(image_product)

        # Delete Linked Image Records
        for image_id in image_ids:
            other_links = ImageProduct.query.filter_by(image_id=image_id).count()
            if other_links == 0:
                image = Image.query.get(image_id)
                if image:
                    db.session.delete(image)
        
        # Delete Associated OrderProduct Records
        OrderProduct.query.filter_by(product_id=product_id).delete()

        # Delete Product
        db.session.delete(product)

        # Commit Changes
        db.session.commit()

        return jsonify({
            'success': True
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


# Replace with Pagination Approach
@product_bp.route('/get_all_products', methods=['GET'])
def get_all_products():
    try:
        # Load All Products with image_ids
        products = Product.query.options(
            joinedload(Product.image_ids).joinedload(ImageProduct.image)
        ).all()
        
        # If No Products Exist, Return Empty List
        if not products:
            return jsonify({
                'success': True,
                'data': []
            }), 200
        
        # Serialize Products
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