from flask import Blueprint, request, jsonify
from flask_app.extensions import db
from flask_app.models import Product, Order, User, OrderProduct
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
import sys
from werkzeug.utils import secure_filename
from flask_app.models import Img

image_bp = Blueprint('images', __name__)

ALLOWED_MIMETYPES = {'image/jpeg', 'image/png', 'image/gif'}

@image_bp.route('/upload_single_file', methods=['POST'])
def upload_single_file():
    try:
        file = request.files['file']

        # Check if File Exsists
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({
                'success': False,
                'error': 'No Image Uploaded'
            }), 400
        
        # Validate Minetype
        if file.mimetype not in ALLOWED_MIMETYPES:
            return jsonify({
                'success': False,
                'error': 'Invalid File Type. Only JPEG, PNG, and GIF are Allowed'
            }), 400
        
        # Validate file size (e.g., max 5MB)
        file.seek(0, 2)
        file_size = file.tell()
        max_size = 5 * 1024 * 1024  # 5MB
        if file_size > max_size:
            return jsonify({
                'success': False,
                'error': 'File Too Large. Maximum Size is 5MB'
            }), 413
        file.seek(0) 
        
        img = Img(
            img=file.read(), 
            mimetype=file.mimetype, 
            name=file.filename
        )

        db.session.add(img)
        db.session.commit()

        return jsonify({
                'success': True,
                'message': 'Image Uploaded Successfully',
            }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to Upload',
            'message': str(e)
        }), 500
    

@image_bp.route('/upload_multible_files', methods=['POST'])
def upload_multible_files():
    try:
        # Check if File Exsists
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No Images Uploaded'
            }), 400
        
        files = request.files.getlist('files')
        image_ids = []
        max_size = 5 * 1024 * 1024  # 5MB

        if not files or all(file.filename == '' for file in files):
            return jsonify({
                'success': False,
                'error': 'Invalid File Uploaded'
            }), 400
        
        for file in files:
            if file.mimetype not in ALLOWED_MIMETYPES:
                return jsonify({
                    'success': False,
                    'error': f'Invalid File Type for {file.filename}. Only JPEG, PNG, and GIF are Allowed'
                }), 400

            file.seek(0, 2)
            file_size = file.tell()
            if file_size > max_size:
                return jsonify({
                    'success': False,
                    'error': f'File {file.filename} Too Large. Maximum Size is 5MB'
                }), 413
            file.seek(0)

            img = Img(
                img=file.read(),
                mimetype=file.mimetype,
                name=file.filename
            )
            
            db.session.add(img)
            db.session.flush()
            image_ids.append(img.id)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Images Uploaded Successfully',
            'imageIds': image_ids
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to Upload',
            'message': str(e)
        }), 500