from flask import Blueprint, request, jsonify
from flask_app.extensions import db
from flask_app.models import Product, Order, User

order_control_bp = Blueprint('ordersControl', __name__)

# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)


#NON CLAIM ORDERS ROUTE  
# to display orders that haven't been claimed yet.
@order_control_bp.route('/unclaimed', methods=['GET'])
def get_unclaimed_orders():
    try:
        # Query all unclaimed orders (status 'pending' and no employee assigned)
        unclaimed_orders = Order.query.filter_by(status='pending', claimed_by_employee_id=None).order_by(Order.id.asc()).all()

        # If no orders are found, return an error or empty list (here we mimic get_all_orders)
        if not unclaimed_orders:
            return jsonify({
                'success': False,
                'error': 'No unclaimed orders found'
            }), 404

        # Convert orders to a list of dictionaries with product details
        order_data = []
        for order in unclaimed_orders:
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
                "created_at": order.created_at.isoformat()  # Ensuring timestamp is serializable
            }
            order_data.append(order_info)

        return jsonify({
            'success': True,
            'orders': order_data
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch unclaimed orders',
            'message': str(e)
        }), 500



#ADD ORDER TO EMPLOYEE DASHBOARD
#to display the orders claimed by a specific employee.
# ADD ORDER TO EMPLOYEE DASHBOARD
# to display the orders claimed by a specific employee.
@order_control_bp.route('/employeeDashboard/<int:employee_id>', methods=['GET'])
def get_employee_dashboard(employee_id):
    try:
        # Fetch all orders claimed by this employee (using the correct field name)
        claimed_orders = Order.query.filter_by(claimed_by_employee_id=employee_id).order_by(Order.id.desc()).all()
       
        # Convert orders to a list of dictionaries with product details
        order_data = []
        for order in claimed_orders:
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
                "created_at": order.created_at.isoformat()
            }
            order_data.append(order_info)
       
        # Always return a successful response with an empty array if no orders are found
        return jsonify({
            'success': True,
            'orders': order_data
        }), 200


    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch claimed orders for employee',
            'message': str(e)
        }), 500


@order_control_bp.route('/claim', methods=['POST'])
def claim_order():
    # The ID of the order to claim
    order_id = request.json.get('order_id')
    # The ID of the employee claiming the order
    employee_id = request.json.get('employee_id')
    
    # Fetch the order from the database
    order = Order.query.get(order_id)
    if not order:
        return jsonify({
            'success': False,
            'error': 'Order not found'
        }), 404
    
    if order.status != 'pending':
        return jsonify({
            'success': False,
            'error': 'Order has already been claimed'
        }), 400
    
    # Update the order status and assign the employee using the correct field name
    order.status = 'claimed'
    order.claimed_by_employee_id = employee_id
    
    # Commit the changes to the database
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Order Claimed Successfully'
    }), 200


@order_control_bp.route('/unclaim', methods=['POST'])
def unclaim_order():
    # Retrieve the order ID from the request
    order_id = request.json.get('order_id')
    if not order_id:
        return jsonify({
            'success': False,
            'error': 'Order ID not Found'
        }), 400

    # Fetch the order from the database
    order = Order.query.get(order_id)
    if not order:
        return jsonify({
            'success': False,
            'error': 'Order not Found'
        }), 404

    # Check if the order is actually claimed before attempting to unclaim it
    if order.status not in ['claimed', 'working', 'confirmed']:
        return jsonify({
            'success': False,
            'error': 'Order is not Claimed'
        }), 400

    # Revert the order's status to 'pending' and remove the employee assignment
    order.status = 'pending'
    order.claimed_by_employee_id = None

    # Commit the changes to the database
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Order Unclaimed Successfully'
    }), 200


#RETRIEVE ORDER DETAILS (PARAM: ORDER_ID)
@order_control_bp.route('/orderDetails/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    try:
        # Fetch the order by its ID
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404

        # Build the order info dictionary
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
            "created_at": order.created_at.isoformat()
        }

        # Return the order details
        return jsonify({
            'success': True,
            'order': order_info
        }), 200


    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch order details',
            'message': str(e)
        }), 500

@order_control_bp.route('/confirm', methods=['POST'])
def confirm_order():
    # The ID of the order to confirm
    order_id = request.json.get('order_id')
    # The ID of the employee confirming the order
    employee_id = request.json.get('employee_id')
    
    # Fetch the order from the database
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    # Ensure the order is in the claimed state before confirming
    if order.status != 'working':
        return jsonify({"error": "Order is not in a claimed state"}), 400
    
    # Update the order status to 'confirmed'
    order.status = 'confirmed'
    db.session.commit()
    
    return jsonify(order.to_dict()), 200


@order_control_bp.route('/working', methods=['POST'])
def working_order():
    # The ID of the order to move to working state
    order_id = request.json.get('order_id')
    # The ID of the employee processing the order
    employee_id = request.json.get('employee_id')
    
    # Fetch the order from the database
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    # Ensure the order is in the confirmed state before marking as working
    if order.status != 'claimed':
        return jsonify({"error": "Order is not in a confirmed state"}), 400
    
    # Update the order status to 'working'
    order.status = 'working'
    db.session.commit()
    
    return jsonify(order.to_dict()), 200