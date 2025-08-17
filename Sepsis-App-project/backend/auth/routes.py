import os
from flask import request, jsonify, session, Blueprint, current_app, redirect, url_for
from functools import wraps
from sqlalchemy.exc import IntegrityError
from models import db, bcrypt, User # Import các đối tượng từ models.py
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from authlib.integrations.flask_client import OAuth

auth_bp = Blueprint('auth', __name__)

def normalize_email(raw: str) -> str:
    """Chuẩn hóa email về dạng chữ thường và loại bỏ khoảng trắng."""
    return (raw or '').strip().lower()

# ---- Decorator bảo vệ route bằng JWT (được khuyến nghị) ----
# Bạn nên sử dụng @jwt_required() của Flask-JWT-Extended
# để bảo vệ các route cần xác thực.
# Decorator 'login_required' dựa trên session có thể bị loại bỏ
# nếu bạn chuyển hoàn toàn sang JWT.
def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        # Đây là kiểm tra session cũ. Nếu bạn đã chuyển sang JWT,
        # bạn có thể loại bỏ hoặc thay thế nó bằng logic kiểm tra JWT.
        if 'user_id' not in session:
             return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return wrapped

# ---- Register (đăng ký qua email và password) ----
@auth_bp.route('/register', methods=['POST'])
def register():
    """Xử lý đăng ký người dùng mới với email và mật khẩu."""
    data = request.get_json(silent=True) or {}
    email = normalize_email(data.get('email'))
    password = (data.get('password') or '').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(email=email, password_hash=password_hash)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': 'User registered successfully',
            'user': {'id': user.id, 'email': user.email}
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 409
    except Exception as e:
        db.session.rollback()
        print(f"REGISTER ERROR: {repr(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# ---- Login qua Email và Password ----
@auth_bp.route('/login', methods=['POST'])
def login():
    """Xử lý đăng nhập người dùng bằng email và mật khẩu, trả về JWT."""
    data = request.get_json(silent=True) or {}
    email = normalize_email(data.get('email'))
    password = (data.get('password') or '').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.id)

    # Khi sử dụng JWT, việc lưu session thường không cần thiết cho xác thực.
    # Frontend sẽ quản lý JWT. Đoạn dưới đây chỉ giữ lại nếu bạn có lý do đặc biệt.
    session.clear()
    session['user_id'] = user.id
    session['user_email'] = user.email

    return jsonify({
        'message': 'Logged in successfully',
        'access_token': access_token, # Trả về token JWT
        'user': {'id': user.id, 'email': user.email}
    }), 200

# ---- Login qua Google OAuth ----
@auth_bp.route('/google_login')
def google_login():
    """Khởi tạo quá trình đăng nhập Google OAuth."""
    oauth_instance = current_app.extensions['authlib.integrations.flask_client']
    
    # SỬA LỖI TẠI ĐÂY: Chuyển hướng đến 'auth.google_callback'
    redirect_uri = url_for('auth.google_callback', _external=True) 
    current_app.logger.debug(f"Redirect URI being used: {redirect_uri}")
    return oauth_instance.google.authorize_redirect(redirect_uri)



# ---- Logout ----
@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Xử lý đăng xuất người dùng bằng cách xóa session."""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

# ---- Lấy profile của chính mình ----
@auth_bp.route('/me', methods=['GET'])
@jwt_required() # Yêu cầu JWT để truy cập route này
def me():
    """Lấy thông tin profile của người dùng hiện tại (dựa trên JWT)."""
    current_user_id = get_jwt_identity() # Lấy user_id từ token JWT
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'profile_picture': user.profile_picture
    }), 200

@auth_bp.route('/check_oauth_status', methods=['GET'])
def check_oauth_status():
    """
    Route để kiểm tra xem đối tượng OAuth đã được khởi tạo và
    đăng ký đúng cách trong current_app.extensions hay chưa.
    """
    # Đã sửa lỗi: Khóa chính xác là 'authlib.integrations.flask_client'
    oauth_key = 'authlib.integrations.flask_client'
    
    # Kiểm tra xem key có tồn tại trong extensions không
    is_oauth_registered = oauth_key in current_app.extensions
    
    oauth_instance = None
    if is_oauth_registered:
        oauth_instance = current_app.extensions[oauth_key]
        
    return jsonify({
        'status': 'success',
        'message': 'OAuth registration check completed.',
        'is_authlib_oauth_registered_in_extensions': is_oauth_registered,
        'oauth_instance_type': str(type(oauth_instance)) if oauth_instance else None,
        'all_extensions_keys': list(current_app.extensions.keys()) # Liệt kê tất cả các keys trong extensions
    }), 200


# Route callback để xử lý phản hồi từ Google
@auth_bp.route('/google/callback')
def google_callback():
    """
    Xử lý phản hồi từ Google sau khi người dùng đăng nhập và cấp quyền.
    Đổi mã ủy quyền lấy access token và thông tin người dùng.
    """
    oauth = current_app.extensions['authlib.integrations.flask_client']
    google = oauth.google

    try:
        # Lấy access token và thông tin người dùng từ Google
        # Authlib sẽ tự động xử lý việc gửi mã ủy quyền và nhận token
        token = google.authorize_access_token()
        userinfo = google.parse_id_token(token) # Lấy thông tin từ ID Token

        # Ghi log thông tin người dùng nhận được (cho mục đích debug)
        current_app.logger.debug(f"User Info from Google: {userinfo}")
        
        # --- Xử lý thông tin người dùng tại đây ---
        # 1. Kiểm tra xem người dùng đã tồn tại trong DB chưa
        # 2. Nếu chưa, tạo người dùng mới
        # 3. Tạo JWT access token cho người dùng

        # Ví dụ: Tạo JWT token cho người dùng
        # Sử dụng 'sub' (subject) từ userinfo làm định danh người dùng
        # 'sub' là ID duy nhất của người dùng Google
        user_id = userinfo['sub'] 
        access_token = create_access_token(identity=user_id, expires_delta=timedelta(hours=1))

        # Trả về JWT token hoặc chuyển hướng người dùng về frontend với token
        # Trong ứng dụng thực tế, bạn sẽ chuyển hướng về frontend với token
        # hoặc trả về JSON chứa token để frontend xử lý.
        return jsonify(access_token=access_token)

    except Exception as e:
        # Ghi log lỗi chi tiết
        current_app.logger.error(f"Google OAuth callback error: {e}")
        # Trả về thông báo lỗi thân thiện cho người dùng
        return jsonify({"msg": "Google OAuth failed", "error": str(e)}), 400