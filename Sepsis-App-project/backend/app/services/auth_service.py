# backend/app/services/auth_service.py
from app.models.models import db, User
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

def _create_jwt_token(user):
    identity = {"id": user.id, "email": user.email, "is_admin": user.is_admin}
    return create_access_token(identity=identity)

def register_user(data):
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()

    if not email or not password: return None, "Yêu cầu email và mật khẩu.", 400
    if len(password) < 6: return None, "Mật khẩu phải có ít nhất 6 ký tự.", 400
    
    try:
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user, "Đăng ký thành công.", 201
    except IntegrityError:
        db.session.rollback()
        return None, "Email đã tồn tại.", 409

def login_user(data):
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        if not user.is_active: return None, "Tài khoản đã bị vô hiệu hóa.", 403
        access_token = _create_jwt_token(user)
        return access_token, "Đăng nhập thành công.", 200
    
    return None, "Sai email hoặc mật khẩu.", 401

def process_google_login(userinfo):
    google_id = userinfo['sub']
    email = userinfo['email']
    user = User.query.filter((User.google_id == google_id) | (User.email == email)).first()

    if user:
        user.google_id = google_id
        user.name = userinfo.get('name')
        user.profile_picture = userinfo.get('picture')
    else:
        user = User(
            google_id=google_id, email=email,
            name=userinfo.get('name'), profile_picture=userinfo.get('picture')
        )
        db.session.add(user)
    
    db.session.commit()
    access_token = _create_jwt_token(user)
    return access_token, "Đăng nhập với Google thành công.", 200