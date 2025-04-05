# from flask import Blueprint, request, jsonify, session
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_app.extensions import db
# from flask_app.models import User
# from email_validator import validate_email, EmailNotValidError
# import re


# # CODES USE:
# # 200: OK - Request succeeded normally
# # 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# # 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# # 401: Unauthorized - Authentication is required and has failed or not been provided
# # 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)




# # #Login required decorator, user "login_required" to protect routes that require authentication
# # def login_required(f):
# #     #use wraps to preserve the name of a funciton while wrapping with a decorator
# #     @wraps(f)


# #     def decorated_function(*args, **kwargs):
# #         if 'user_id' not in session:
# #             return jsonify({
# #                 'success': False,
# #                 'error': 'Must log in before acessing this information'
# #             }), 401
# #         return f(*args, **kwargs)
# #     return decorated_function


# user_bp = Blueprint('user', __name__)


# #validate the password strength


# def validate_password(password):
#     """
#     Validate password strength:
#     - At least 8 characters long
#     - Contains at least one uppercase letter
#     - Contains at least one lowercase letter
#     - Contains at least one number
#     - Contains at least one special character
#     """
#     if len(password) < 8:
#         return False
   
#     if not re.search(r'[A-Z]', password):
#         return False
   
#     if not re.search(r'[a-z]', password):
#         return False
   
#     if not re.search(r'\d', password):
#         return False
   
#     if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
#         return False
   
#     return True


# @user_bp.route('/signup', methods=['POST'])
# def signup():
#     try:
#         data = request.get_json()


#         # Check if required fields are present
#         if not all(k in data for k in ['username', 'password', 'email', 'name']):
#             return jsonify({
#                 'success': False,
#                 'error': 'Missing required fields'
#             }), 400
       
#         # Validate email format
#         try:
#             valid = validate_email(data['email'])
#             validated_email = valid.email  # Normalized email
#         except EmailNotValidError as e:
#             return jsonify({
#                 'success': False,
#                 'error': f'Invalid email format: {str(e)}'
#             }), 400


#         # Validate password strength
#         if not validate_password(data['password']):
#             return jsonify({
#                 'success': False,
#                 'error': 'Password must be at least 8 characters long and include uppercase, lowercase, number, and special character'
#             }), 400


#         # Check if username already exists
#         if User.query.filter_by(username=data['username']).first():
#             return jsonify({
#                 'success': False,
#                 'error': 'Username already exists'
#             }), 400


#         # Check if email already exists (using validated email)
#         if User.query.filter_by(email=validated_email).first():
#             return jsonify({
#                 'success': False,
#                 'error': 'Email already exists'
#             }), 400


#         # Create new user (using validated email)
#         new_user = User(
#             name=data['name'],
#             username=data['username'],
#             email=validated_email,  # Use validated email
#             password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
#             user_type='customer'
#         )


#         # Add to database
#         db.session.add(new_user)
#         db.session.commit()


#         return jsonify({
#             'success': True,
#             'message': 'User created successfully',
#             'user': new_user.to_dict()
#         }), 201


#     except Exception as e:
#         db.session.rollback()
#         return jsonify({
#             'success': False,
#             'error': 'Failed to create user',
#             'message': str(e)
#         }), 500
   
# @user_bp.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.get_json()


#         if not all(k in data for k in ['email', 'password']):
#             return jsonify({
#                 'success': False,
#                 'error': 'Missing required fields'
#             }), 400
       
#         # Validate email format
#         try:
#             valid = validate_email(data['email'])
#             validated_email = valid.email  # Normalized email
#         except EmailNotValidError as e:
#             return jsonify({
#                 'success': False,
#                 'error': f'Invalid email format: {str(e)}'
#             }), 400


#         # Find user by validated email
#         user = User.query.filter_by(email=validated_email).first()


#         if user and check_password_hash(user.password, data['password']):
#             return jsonify({
#                 'success': True,
#                 'message': 'Login successful',
#                 'user': user.to_dict()
#             }), 200
#         else:
#             return jsonify({
#                 'success': False,
#                 'error': 'Invalid email or password'
#             }), 401


#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': 'Login failed',
#             'message': str(e)
#         }), 500


from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app.extensions import db
from flask_app.models import User
from email_validator import validate_email, EmailNotValidError
import re


user_bp = Blueprint('user', __name__)


def validate_password(password):
    """
    Validate password strength:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character
    """
    if len(password) < 8:
        return False
   
    if not re.search(r'[A-Z]', password):
        return False
   
    if not re.search(r'[a-z]', password):
        return False
   
    if not re.search(r'\d', password):
        return False
   
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
   
    return True


@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()


        # Check if required fields are present
        if not all(k in data for k in ['username', 'password', 'email', 'name']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
       
        #Validate email format
        try:
            valid = validate_email(data['email'])
            validated_email = valid.email  # Normalized email
        except EmailNotValidError as e:
            return jsonify({
                'success': False,
                'error': f'Invalid email format: {str(e)}'
            }), 400






        # Validate password strength
        if not validate_password(data['password']):
            return jsonify({
                'success': False,
                'error': 'Password must be at least 8 characters long and include uppercase, lowercase, number, and special character'
            }), 400


        # Check if username already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'success': False,
                'error': 'Username already exists'
            }), 400


        # Check if email already exists (using validated email)
        if User.query.filter_by(email=validated_email).first():
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 400


        # Create new user (using validated email)
        new_user = User(
            name=data['name'],
            username=data['username'],
            email=validated_email,  # Use validated email
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
       
        # Validate email format
        try:
            valid = validate_email(data['email'])
            validated_email = valid.email  # Normalized email
        except EmailNotValidError as e:
            return jsonify({
                'success': False,
                'error': f'Invalid email format: {str(e)}'
            }), 400


        # Find user by validated email
        user = User.query.filter_by(email=validated_email).first()


        ##########################################
        # EMPLOYEE USER


        employee_list = {
            "kimmy.sullivan@gmail.com":{
                "name": "Kimmy Sullivan",
                "password": "KimmyS123!"
            },
           
            "donna.kind@gmail.com":{
                "name": "Donna Kind",
                "password": "DonnaK456!"
    }
        }
       
        is_employee = validated_email in employee_list
       
        # # If this is the first login for an employee, create their account
        # if is_employee and not user:
        #     employee_name = employee_list[validated_email]
        #      # Use part before @ as username
        #     username = validated_email.split('@')[0]
           
        #     # Create employee user
        #     user = User(
        #         name=employee_name,
        #         username=username,
        #         email=validated_email,
        #         password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
        #         user_type='employee'
        #     )
           
        #     db.session.add(user)
        #     db.session.commit()


        #     # If it's an existing employee, update their type if needed
        # elif is_employee and user and user.user_type != 'employee':
        #     user.user_type = 'employee'
        #     db.session.commit()


        if is_employee:
            if not user:  # Employee is logging in for the first time
                employee_name = employee_list[validated_email]["name"]
                username = validated_email.split('@')[0]


                user = User(
                    name=employee_name,
                    username=username,
                    email=validated_email,
                    password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
                    user_type='employee'
                )
                db.session.add(user)
                db.session.commit()
            # Existing user but wrong type
            elif user.user_type != 'employee':
                user.user_type = 'employee'
                db.session.commit()                      




            #########################################


        if user and check_password_hash(user.password, data['password']):


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


@user_bp.route('/get_users')
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@user_bp.route('/deleteUser', methods=['DELETE'])
def deleteUser():

    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({"error": "User ID required"}), 400
    
    user_id = int(data['id'])
    print(f"Deleting user with ID: {user_id}")
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully :)"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user_bp.route('/createUser', methods=['POST'])
def createUser():

    data = request.get_json()

    if not all(k in data for k in ['username', 'password', 'email', 'name', 'usertype']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
       
    #Validate email format
    try:
        valid = validate_email(data['email'])
        validated_email = valid.email  # Normalized email
    except EmailNotValidError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid email format: {str(e)}'
        }), 400
    

    # Validate password strength
    if not validate_password(data['password']):
        return jsonify({
            'success': False,
            'error': 'Password must be at least 8 characters long and include uppercase, lowercase, number, and special character'
        }), 400


    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'success': False,
            'error': 'Username already exists'
        }), 400
    
    # Check if email already exists (using validated email)
    if User.query.filter_by(email=validated_email).first():
        return jsonify({
            'success': False,
            'error': 'Email already exists'
        }), 400


    new_user = User(
        name=data['name'],
        username=data['username'],
        email=validated_email,  # Use validated email
        password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
        user_type=data['usertype']
    )


        # Add to database
    db.session.add(new_user)
    db.session.commit()


    return jsonify({
        'success': True,
        'message': 'User created successfully',
        'user': new_user.to_dict()
    }), 201



