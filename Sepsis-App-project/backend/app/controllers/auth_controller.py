# backend/app/controllers/auth_controller.py
from flask import request, jsonify, url_for, current_app
from app.services import auth_service
from app.models.models import User
from flask_jwt_extended import get_jwt_identity
from main import oauth

def register():
    user, message, status_code = auth_service.register_user(request.get_json())
    if not user: return jsonify({"message": message}), status_code
    return jsonify({"message": message, "user": user.to_dict()}), status_code

def login():
    token, message, status_code = auth_service.login_user(request.get_json())
    if not token: return jsonify({"message": message}), status_code
    return jsonify(access_token=token, message=message), status_code

def google_login():
    
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

def google_callback():
   
    try:
        token_data = oauth.google.authorize_access_token()
        userinfo = oauth.google.parse_id_token(token_data)
        access_token, message, status_code = auth_service.process_google_login(userinfo)
        return jsonify(access_token=access_token, message=message), status_code
    except Exception as e:
        return jsonify({"message": "Đăng nhập Google thất bại", "error": str(e)}), 400

def get_me():
    user_id = get_jwt_identity()['id']
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200
