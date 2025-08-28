# backend/app/services/auth_service.py
from app.models.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token, decode_token
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from datetime import timedelta
import os
import logging
from flask import current_app

def _create_jwt_token(user):
    # Sửa lỗi: Ép kiểu identity thành string để đảm bảo tương thích
    identity = str(user.id)
    additional_claims = {"role": user.role, "username": user.username}
    return create_access_token(identity=identity, additional_claims=additional_claims)

def forgot_password(data):
    """Xử lý yêu cầu quên mật khẩu. Chỉ soạn email, không gửi."""
    email = (data.get('email') or '').strip().lower()
    user = User.query.filter_by(email=email).first()

    if user:
        reset_token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=15))
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        reset_url = f"{frontend_url}/reset-password?token={reset_token}"
        
        email_data = {
            "subject": "Yêu cầu Đặt lại Mật khẩu - SepsIS+",
            "recipients": [user.email],
            "body": f'''Để đặt lại mật khẩu của bạn, hãy truy cập vào đường link sau:
{reset_url}

Nếu bạn không phải là người yêu cầu, xin hãy bỏ qua email này.
'''
        }
        return True, email_data, 200
    
    return True, None, 200

def reset_password(data):
    """Xử lý đặt lại mật khẩu với token."""
    token = data.get('token')
    new_password = data.get('new_password')

    if not token or not new_password:
        return False, "Yêu cầu token và mật khẩu mới.", 400

    try:
        decoded_token = decode_token(token)
        # Sửa lỗi: Kiểm tra sự tồn tại của 'sub' và chuyển kiểu an toàn
        user_id_str = decoded_token.get('sub')
        if not user_id_str:
            return False, "Token không hợp lệ (thiếu thông tin người dùng).", 401
        
        user_id = int(user_id_str)
        user = User.query.get(user_id)

        if not user:
            return False, "Người dùng không tồn tại.", 404

        user.set_password(new_password)
        db.session.commit()
        return True, "Đặt lại mật khẩu thành công.", 200

    except Exception as e:
        return False, f"Token không hợp lệ hoặc đã hết hạn: {str(e)}", 401

def register_user(data):
    username = data.get('username')
    email = (data.get('email') or '').strip().lower()
    password = data.get('password')

    if not all([username, email, password]):
        return None, "Tài khoản, email và mật khẩu là bắt buộc.", 400
    if User.query.filter_by(username=username).first():
        return None, "Tài khoản đã tồn tại.", 409
    if User.query.filter_by(email=email).first():
        return None, "Email đã tồn tại.", 409
    
    new_user = User(
        username=username,
        email=email,
        name=data.get('name'),
        phone=data.get('phone'),
        role=data.get('role', 'Staff')
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user, "Đăng ký thành công.", 201

def login_user(data):
    # Cập nhật: Đăng nhập bằng username
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        if not user.is_active: return None, "Tài khoản đã bị vô hiệu hóa.", 403
        access_token = _create_jwt_token(user)
        return access_token, "Đăng nhập thành công.", 200
    
    return None, "Sai tài khoản hoặc mật khẩu.", 401

def process_google_login(userinfo):
    """
    Xử lý đăng nhập Google. Chỉ cho phép đăng nhập nếu email đã tồn tại.
    """
    email = userinfo['email']
    
    # Bước 1: Tìm người dùng bằng email
    user = User.query.filter_by(email=email).first()

    # Bước 2: Nếu không tìm thấy, trả về lỗi
    if not user:
        return None, "Tài khoản của bạn không tồn tại trong hệ thống.", 403 # Forbidden

    # Bước 3: Nếu tìm thấy, liên kết tài khoản và cập nhật thông tin
    user.google_id = userinfo['sub'] # Liên kết Google ID
    user.name = userinfo.get('name', user.name)
    user.profile_picture = userinfo.get('picture', user.profile_picture)
    
    db.session.commit()
    
    # Bước 4: Tạo token và trả về
    access_token = _create_jwt_token(user)
    return access_token, "Đăng nhập với Google thành công.", 200