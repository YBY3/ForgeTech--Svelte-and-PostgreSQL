from flask import Blueprint, request, jsonify
from flask_app.extensions import db
from flask_app.models import Product, Order

order_bp = Blueprint('orders', __name__)


# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)


@order_bp.route('/add_order', methods=['POST'])
def add_order():
    try:
        data = request.get_json()

        # Checks for Missing Data
        if not data or 'product_ids' not in data or 'total' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing Order Data'
            }), 400

        # Link Product Ids
        products = Product.query.filter(Product.id.in_(data['product_ids'])).all()

        if not products:
            return jsonify({
                'success': False,
                'error': 'Selected Products Are Not In the Database'
            }), 404

        # Create a new Order
        new_order = Order(
            user_id=data['user_id'],
            products=products,
            total=data['total'],
            status=data['status']
        )

        # Add to the Database
        db.session.add(new_order)
        db.session.commit()

        # Return a Confirmation Message
        return jsonify({
            'success': True,
            'message': 'Order Added'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to Add Order',
            'message': str(e)
        }), 500
    

# remove_order route
# goal: remove order via order id


# get_all_orders route
# goal: get all orders via user id