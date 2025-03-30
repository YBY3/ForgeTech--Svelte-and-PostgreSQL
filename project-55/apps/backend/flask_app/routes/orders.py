from flask import Blueprint, request, jsonify
from flask_app.extensions import db
from flask_app.models import Product, Order, User




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




@order_bp.route('/get_all_orders', methods=['POST'])
def get_all_orders():
    try:
        data = request.get_json()

        # Validate Request Body
        if not data or 'user_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing user_id in request'
            }), 400

        user_id = data['user_id']

        # Query all orders for the given user ID, including products
        past_orders = Order.query.filter_by(user_id=user_id).order_by(Order.id.desc()).all()

        # Check if any orders exist
        if not past_orders:
            return jsonify({
                'success': False,
                'error': 'No orders found for this user'
            }), 404

        # Convert orders to a list of dictionaries with product details
        order_data = []
        for order in past_orders:
            order_info = {
                "id": order.id,
                "user_id": order.user_id,
                "total": order.total,
                "status": order.status,
                "products": [
                    {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                    } for product in order.products
                ],
                "created_at": order.created_at.isoformat()  # Ensure timestamp is serializable
            }
            order_data.append(order_info)

        return jsonify({
            'success': True,
            'orders': order_data
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch orders',
            'message': str(e)
        }), 500
