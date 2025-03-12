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
        # orders = Order.query.filter_by(user_id=user_id).all()
        past_orders = Order.query.filter_by(user_id=user_id).order_by(Order.id.desc()).all()
    



        # Check if any orders exist
        if not orders:
            return jsonify({
                'success': False,
                'error': 'No orders found for this user'
            }), 404


        # Convert orders to a list of dictionaries with product details
        order_data = []
        for order in orders:
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
                ]
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
   


#NON CLAIM ORDERS ROUTE  
# to display orders that haven't been claimed yet.


@order_bp.route('/orders/unclaimed', methods=['GET'])
def get_unclaimed_orders():
    # Fetch all unclaimed orders (status 'Pending' and no employee assigned)
    unclaimed_orders = Order.query.filter_by(status='Pending', employee_id=None).order_by(Order.id.asc()).all()
   
    # Return the orders as a JSON response
    return jsonify([order.to_dict() for order in unclaimed_orders])


#CLAIM ORDER ROUTE
#to allow an employee to claim an order by updating its status and assigning it to the employee
@order_bp.route('/orders/claim', methods=['POST'])
def claim_order():
    # The ID of the order to claim
    order_id = request.json.get('order_id')  
     # The ID of the employee claiming the order
    employee_id = request.json.get('employee_id')
   
    # Fetch the order from the database
    order = Order.query.get(order_id)
   
    if not order:
        return jsonify({"error": "Order not found"}), 404
   
    if order.status != 'Pending':
        return jsonify({"error": "Order has already been claimed"}), 400
   
    # Update the order status and assign the employee
    order.status = 'Claimed'
    order.employee_id = employee_id
   
    # Commit the changes to the database
    db.session.commit()
   
    return jsonify(order.to_dict())


#ADD ORDER TO EMPLOYEE DASHBOARD
#to display the orders claimed by a specific employee.


@order_bp.route('/employee/<int:employee_id>/dashboard', methods=['GET'])
def get_employee_dashboard(employee_id):
    try:
        # Fetch all orders claimed by this employee (where employee_id is set)
        claimed_orders = Order.query.filter_by(employee_id=employee_id).order_by(Order.id.desc()).all()
       
        if not claimed_orders:
            return jsonify({
                'success': False,
                'message': 'No orders found for this employee'
            }), 404
       
        # Format the orders into a list of dictionaries
        order_data = [order.to_dict() for order in claimed_orders]
       
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



