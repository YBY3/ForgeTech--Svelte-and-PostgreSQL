# from flask import Blueprint
# from .extensions import db
# from .models import Product
# from .models import User
# from werkzeug.security import check_password_hash

# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)

#imported blueprint to organize the flask app into smaller components allowing the use of the main routw
#imported request to access incoming HTTP requests
#imported jsonify to convert python dictionaries to JSON
#imported session to store data for a user session
from flask import Blueprint, request, jsonify, session
#imported generate_password_hash and check_password_hash to hash passwords
from werkzeug.security import generate_password_hash, check_password_hash
# imported wraps to create a decorator
from functools import wraps
# imported db to access the database
from .extensions import db
# imported User and Product models
from .models import User, Product, Order

#created a blueprint called main
main = Blueprint('main', __name__)

#Login required decorator, user "login_required" to protect routes that require authentication
def login_required(f):
    #use wraps to preserve the name of a funciton while wrapping with a decorator
    @wraps(f)

    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'error': 'Must log in before acessing this information'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

@main.route('/products')
# @login_required (Commented out for testing purposes. Enable once done)
def get_products():
    products = Product.query.all()
    productData = [product.to_dict() for product in products]
    return jsonify(productData)

@main.route('/users')
@login_required  
def get_users():
    users = User.query.all()
    userData = [user.to_dict() for user in users]
    return jsonify(userData)


@main.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        # Check if required fields are present
        if not all(k in data for k in ['username', 'password', 'email']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400

        # Check if username already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'success': False,
                'error': 'Username already exists'
            }), 400

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 400

        # Create new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'], method='pbkdf2:sha256')
        )

        # Add to database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to create user',
            'message': str(e)
        }), 500

@main.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not all(k in data for k in ['username', 'password']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400

        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            # Store user id in session
            session['user_id'] = user.id  
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Login failed',
            'message': str(e)
        }), 500
       
@main.route('/logout')
def logout():
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200

# #product route within the main route
# @main.route('/products')
# def get_products():
#     products = Product.query.all()
#     productData = [product.to_dict() for product in products]
#     return productData

# #user route within blueprint 
# @main.route('/users')
# def get_users():
#     users = User.query.all()
#     Userdata = [user.to_dict() for user in users]
#     return Userdata

@main.route('/orders/confirm', methods=['POST'])
# @login_required (Commented out for testing purposes. Enable once done)
def confirm_order():
    """
    This endpoint confirms the placement of an order.
    It requires a logged-in user (checked by login_required).
    The expected JSON payload should include:
      - "order_items": a list of product dictionaries
      - "total": the total price of the order
    """
    try:
        data = request.get_json()

        # Validate that required order data is provided
        if not data or 'order_items' not in data or 'total' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing order data'
            }), 400

        # Get the user_id from the session (set during login)
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401

        # Create a new Order with the provided order items and total
        new_order = Order(
            user_id=user_id,
            order_items=data['order_items'],
            total=data['total'],
            status='Placed'
        )

        # Add to the database
        db.session.add(new_order)
        db.session.commit()

        # Return a confirmation message with a redirect URL.
        return jsonify({
            'success': True,
            'message': 'Order placed successfully.',
            'redirect': '/order-confirmation'  # Home Page for now
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to place order',
            'message': str(e)
        }), 500