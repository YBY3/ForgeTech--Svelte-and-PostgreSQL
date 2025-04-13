from flask import Blueprint, Response, jsonify
from flask_app.models import Image

# CODES USE:
# 200: OK - Request succeeded normally
# 201: Created - Request succeeded and a new resource was created (used in signup when a new user is created)
# 400: Bad Request - Server couldn't understand the request (used when required fields are missing)
# 401: Unauthorized - Authentication is required and has failed or not been provided
# 500: Internal Server Error - Server encountered an unexpected condition (used in catch blocks)


image_bp = Blueprint('images', __name__)
ALLOWED_MIMETYPES = {'image/jpeg', 'image/png', 'image/gif'}


@image_bp.route('/<int:id>')
def fetch_image(id):
    image = Image.query.filter_by(id=id).first()
    if not image:
        return jsonify({
            'success': False,
            'error': 'Failed to Fetch Image'
        }), 404
    
    return Response(image.image, mimetype=image.mimetype)