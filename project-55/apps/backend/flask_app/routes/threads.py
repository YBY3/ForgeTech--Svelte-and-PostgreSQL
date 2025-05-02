from flask import Blueprint, request, jsonify
import sys, json, base64
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
from flask_app.models import Message, Thread, User
from flask_app.extensions import db


# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)


thread_bp = Blueprint('threads', __name__)


@thread_bp.route('/get_threads', methods=['GET'])
def get_threads():
    try:
        # Get query parameters
        user_id = request.args.get('user_id', type=int)
        thread_id = request.args.get('thread_id', type=int)

        # Validate input
        if not user_id and not thread_id:
            return jsonify({
                'success': False,
                'error': 'Missing Parameters',
                'message': 'At least one of user_id or thread_id must be provided'
            }), 400

        if user_id and thread_id:
            # Prioritize thread_id for single-thread retrieval
            thread = Thread.query.get(thread_id)
            if not thread:
                return jsonify({
                    'success': False,
                    'error': 'Thread Not Found',
                    'message': f'Thread with ID {thread_id} does not exist'
                }), 404

            return jsonify({
                'success': True,
                'thread': {
                    'id': thread.id,
                    'name': thread.name,
                    'created_by_id': thread.created_by_id,
                    'username': thread.creator.username,
                    'created_at': thread.created_at.isoformat()
                }
            }), 200

        if thread_id:
            # Single thread by thread_id
            thread = Thread.query.get(thread_id)
            if not thread:
                return jsonify({
                    'success': False,
                    'error': 'Thread Not Found',
                    'message': f'Thread with ID {thread_id} does not exist'
                }), 404

            return jsonify({
                'success': True,
                'thread': {
                    'id': thread.id,
                    'name': thread.name,
                    'created_by_id': thread.created_by_id,
                    'username': thread.creator.username,
                    'created_at': thread.created_at.isoformat()
                }
            }), 200

        if user_id:
            # Multiple threads by user_id
            user = User.query.get(user_id)
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User Not Found',
                    'message': f'User with ID {user_id} does not exist'
                }), 404

            threads = Thread.query.filter_by(created_by_id=user_id).order_by(Thread.created_at.asc()).all()
            return jsonify({
                'success': True,
                'threads': [{
                    'id': thread.id,
                    'name': thread.name,
                    'created_by_id': thread.created_by_id,
                    'username': thread.creator.username,
                    'created_at': thread.created_at.isoformat()
                } for thread in threads]
            }), 200

    except ValueError as ve:
        print(f"ValueError: {str(ve)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Invalid Data Format',
            'message': str(ve)
        }), 400

    except Exception as e:
        print(f"Error Retrieving Threads: {str(e)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Failed to Retrieve Threads',
            'message': str(e)
        }), 500


@thread_bp.route('/add_thread', methods=['POST'])
def add_thread():
    try:
        data = request.get_json()

        # Required fields
        required_fields = ['name', 'user_id']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': 'Missing Thread Info',
                'message': f"Fields missing: {', '.join(missing_fields)}"
            }), 400

        # Validate name
        name = data['name'].strip()
        if not name:
            return jsonify({
                'success': False,
                'error': 'Invalid Thread Name',
                'message': 'Thread name cannot be empty'
            }), 400
        if len(name) > 100:
            return jsonify({
                'success': False,
                'error': 'Invalid Thread Name',
                'message': 'Thread name exceeds 100 characters'
            }), 400

        # Validate user_id
        user_id = data['user_id']
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid User',
                'message': f'User with ID {user_id} does not exist'
            }), 400

        # Check thread limit (max 3 per user)
        user_thread_count = Thread.query.filter_by(created_by_id=user_id).count()
        if user_thread_count >= 3:
            return jsonify({
                'success': False,
                'error': 'Thread Limit Exceeded',
                'message': 'Users can only have up to three threads at a time'
            }), 400

        # Create new thread instance
        thread = Thread(
            name=name,
            created_by_id=user_id
        )

        # Add to database
        db.session.add(thread)
        db.session.commit()

        return jsonify({
            'success': True,
            'thread': {
                'thread_id': thread.id,
                'name': thread.name,
                'created_by_id': thread.created_by_id,
                'username': thread.creator.username,
                'created_at': thread.created_at.isoformat()
            }
        }), 201

    except ValueError as ve:
        print(f"ValueError: {str(ve)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Invalid Data Format',
            'message': str(ve)
        }), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error Adding Thread: {str(e)}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Failed to Add Thread',
            'message': str(e)
        }), 500
    

# Add to Thread (Add Message to Thread)

# Resolve Thread (Employee Only Action)