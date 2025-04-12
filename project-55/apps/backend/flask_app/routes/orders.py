from flask import Blueprint, request, jsonify
from flask_app.extensions import db
from flask_app.models import Product, Order, User, OrderProduct
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
                    products_with_quantity.append({
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": order_item.order_quantity,
                        "images": product.images
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
        return jsonify({
            'success': False,
            'error': 'Failed to fetch orders',
            'message': str(e)
        }), 500
    
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
                        "images": product.images
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