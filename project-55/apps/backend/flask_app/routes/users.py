from flask import Blueprint, request, jsonify, session
#imported generate_password_hash and check_password_hash to hash passwords
from werkzeug.security import generate_password_hash, check_password_hash
# imported wraps to create a decorator
from functools import wraps
# imported db to access the database
from flask_app.extensions import db
# imported User and Product models
from flask_app.models import User

user_bp = Blueprint('user', __name__)


# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)


# #Login required decorator, user "login_required" to protect routes that require authentication
# def login_required(f):
#     #use wraps to preserve the name of a funciton while wrapping with a decorator
#     @wraps(f)

#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             return jsonify({
#                 'success': False,
#                 'error': 'Must log in before acessing this information'
#             }), 401
#         return f(*args, **kwargs)
#     return decorated_function


@user_bp.route('/signup', methods=['POST'])
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
            name=data['name'],
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
            user_type='customer'
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
    

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not all(k in data for k in ['email', 'password']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400

        # Change 'username' to 'email' in the query
        user = User.query.filter_by(email=data['email']).first()

        if user and check_password_hash(user.password, data['password']):
            # Store user id in session
            # session['user_id'] = user.id  
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Login failed',
            'message': str(e)
        }), 500
    
       
# @main.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return jsonify({
#         'success': True,
#         'message': 'Logged out successfully'
#     }), 200