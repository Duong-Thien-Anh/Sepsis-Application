# backend/app/controllers/auth_controller.py
from flask import request, jsonify, url_for, session, current_app
from app.extensions import oauth
from flask_mail import Message
from app.services import auth_service
from app.models.models import User
from flask_jwt_extended import get_jwt_identity
import logging

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
        nonce = session.get('nonce')
        userinfo = oauth.google.parse_id_token(token_data, nonce=nonce)
        
        access_token, message, status_code = auth_service.process_google_login(userinfo)
        return jsonify(access_token=access_token, message=message), status_code
    except Exception as e:
        return jsonify({"message": "Đăng nhập Google thất bại", "error": str(e)}), 400

def get_me():
    # Sửa lỗi: Chuyển identity từ string về lại int để query
    current_user_id_str = get_jwt_identity()
    user_id = int(current_user_id_str)
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

def forgot_password_controller():
    success, email_data, status_code = auth_service.forgot_password(request.get_json())
    
    if email_data:
        try:
            mail = current_app.extensions.get('mail')
            
            msg = Message(**email_data)
            mail.send(msg)
            logging.info(f"Password reset email sent to {email_data['recipients'][0]}")
        except Exception as e:
            logging.error(f"EMAIL SENDING FAILED: {e}", exc_info=True)
            return jsonify({"message": "Lỗi máy chủ khi gửi email."}), 500

    return jsonify({"message": "Nếu email của bạn tồn tại trong hệ thống, một email đặt lại mật khẩu đã được gửi."}), status_code

def reset_password_controller():
    success, message, status_code = auth_service.reset_password(request.get_json())
    if not success:
        return jsonify({"message": message}), status_code
    return jsonify({"message": message}), status_code