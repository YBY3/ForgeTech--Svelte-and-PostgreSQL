from flask import Blueprint, request, jsonify
from flask_app.extensions import db
from flask_app.models import Product, Order, OrderProduct, ImageProduct
from collections import Counter

#Temp Imports
from datetime import datetime
from zoneinfo import ZoneInfo
import sys

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

        # # Checks for Missing Data
        # if (not data) or ('user_id' not in data) or ('items' not in data):
        #     return jsonify({
        #         'success': False,
        #         'error': 'Missing Order Data'
        #     }), 400
        
        user_id = data.get('user_id')
        items = data.get('product_ids')
        total = data.get('total')  

        for item in items:
            product = Product.query.get(item)
            if not product:
                print(f"Product not found for ID: {item}")
                return jsonify({
                    'success': False,
                    'error': f'Product not found for ID: {item}'
                }), 404
        
        #checks if there is enough inventory
        # if product.product_stock < item['quantity']:
        #     return jsonify({
        #         'success': False,
        #         'error': 'Not enough inventory for {product.name}'
        #     }), 400
        
        # # Reduce inventory
        # product.product_stock -= item['quantity']

        # Create a new Order
        new_order = Order(
            user_id= user_id,
            total = total,
            status=data.get('status', 'Pending'),
            arrive_by=datetime.now(ZoneInfo("UTC")) #Temp, should get this datetime from frontend
        )


        # Add to the Database
        db.session.add(new_order)
        # To get the order ID
        db.session.flush()  

        item_counts = Counter(items)
        print(f"Item counts: {item_counts}")

        # Create OrderProduct per product_id
        for product_id, quantity in item_counts.items():
            order_product = OrderProduct(
                order_id=new_order.id,
                product_id=product_id,
                order_quantity=quantity
            )
            db.session.add(order_product)

        db.session.commit()

        # Return a Confirmation Message
        return jsonify({
            'success': True,
            'message': 'Order Added',
            'order_id': new_order.id

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
            # Get order items with quantities
            order_items = OrderProduct.query.filter_by(order_id=order.id).all()

            products_with_quantity = []
            for order_item in order_items:
                product = Product.query.get(order_item.product_id)
                if product:
                    # Fetch image_ids from ImageProduct
                    image_ids = [ip.image_id for ip in ImageProduct.query.filter_by(product_id=product.id).all()]
                    
                    products_with_quantity.append({
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": order_item.order_quantity,
                        "image_ids": image_ids
                    })
            
            order_info = {
                "id": order.id,
                "user_id": order.user_id,
                "total": order.total,
                "status": order.status,
                "arrive_by": order.arrive_by,
                "products": products_with_quantity,
                "created_at": order.created_at.isoformat(),
                "claimed_by_employee_id": order.claimed_by_employee_id
            }
            order_data.append(order_info)

        return jsonify({
            'success': True,
            'orders': order_data
        }), 200

    except Exception as e:
        print(f"Error fetching orders: {str(e)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Failed to fetch orders',
            'message': str(e)
        }), 500
    
# def get_all_orders():
#     try:
#         data = request.get_json()

#         # Validate Request Body
#         if not data or 'user_id' not in data:
#             return jsonify({
#                 'success': False,
#                 'error': 'Missing user_id in request'
#             }), 400

#         user_id = data['user_id']

#         # Query all orders for the given user ID, including products
#         past_orders = Order.query.filter_by(user_id=user_id).order_by(Order.id.desc()).all()

#         # Check if any orders exist
#         if not past_orders:
#             return jsonify({
#                 'success': False,
#                 'error': 'No orders found for this user'
#             }), 404

#         # Convert orders to a list of dictionaries with product details
#         order_data = []
#         for order in past_orders:
#             # Get order items with quantities
#             order_items = OrderProduct.query.filter_by(order_id=order.id).all()

#             products_with_quantity = []
#             for order_item in order_items:
#                 product = Product.query.get(order_item.product_id)
#                 if product:
#                     products_with_quantity.append({
#                         "id": product.id,
#                         "name": product.name,
#                         "price": product.price,
#                         "quantity": order_item.order_quantity,
#                         "image_ids": product.image_ids
#                     })
            
#             order_info = {
#                 "id": order.id,
#                 "user_id": order.user_id,
#                 "total": order.total,
#                 "status": order.status,
#                 "arrive_by": order.arrive_by,
#                 "products": products_with_quantity,
#                 "created_at": order.created_at.isoformat(),
#                 "claimed_by_employee_id": order.claimed_by_employee_id
#             }
#             order_data.append(order_info)

#         return jsonify({
#             'success': True,
#             'orders': order_data
#         }), 200

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': 'Failed to fetch orders',
#             'message': str(e)
#         }), 500
    
# gets orders from all customers
@order_bp.route('/getOrders', methods=['GET'])
def get_orders():
    try:
        all_orders = Order.query.order_by(Order.id.asc()).all()
        print("DEBUG: getOrders retrieved:", all_orders)


        # If no orders are found, return an error or empty list (here we mimic get_all_orders)
        if not all_orders:
            return jsonify({
                'success': False,
                'error': 'No unclaimed orders found'
            }), 404

        # Convert orders to a list of dictionaries with product details
        order_data = []
        for order in all_orders:
            order_items = OrderProduct.query.filter_by(order_id=order.id).all()
            products_with_quantity = []

            for order_item in order_items:
                product = Product.query.get(order_item.product_id)
                if product:
                    products_with_quantity.append({
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": order_item.order_quantity,
                        "image_ids": product.image_ids
                    })
            
            order_info = {
                "id": order.id,
                "user_id": order.user_id,
                "total": order.total,
                "status": order.status,
                "products": products_with_quantity,
                "created_at": order.created_at.isoformat(),
                "arrive_by": order.arrive_by
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
@order_bp.route('/employeeDashboard/<int:employee_id>', methods=['GET'])
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


@order_bp.route('/claim', methods=['POST'])
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


@order_bp.route('/unclaim', methods=['POST'])
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
@order_bp.route('/orderDetails/<int:order_id>', methods=['GET'])
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

@order_bp.route('/confirm', methods=['POST'])
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


@order_bp.route('/working', methods=['POST'])
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
