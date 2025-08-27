# backend/app/services/auth_service.py
from app.models.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

def _create_jwt_token(user):
    # Thêm "camera giám sát" để kiểm tra
    print("--- DEBUG: CREATING TOKEN WITH NEW LOGIC (user.id) ---")
    
    # Sửa lỗi: identity phải là một giá trị đơn giản (như ID)
    identity = user.id
    # Sửa lỗi: Thông tin phụ được đưa vào additional_claims
    additional_claims = {"role": user.role, "username": user.username}
    return create_access_token(identity=identity, additional_claims=additional_claims)

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