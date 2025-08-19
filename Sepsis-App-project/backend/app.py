import os
import logging
import sys # Thêm import sys để sử dụng sys.stdout

from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
from models import db, bcrypt # Import db và bcrypt từ models.py
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth

# ----------------- Bắt đầu phần Cấu hình Logging -----------------
# Cấu hình handler để in log ra console (stdout)
# Điều này đảm bảo log sẽ hiển thị ngay trong terminal của bạn
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Kích hoạt logging DEBUG cho Authlib
# Các sự kiện liên quan đến luồng OAuth của Authlib sẽ được log
log_authlib = logging.getLogger('authlib')
log_authlib.addHandler(handler)
log_authlib.setLevel(logging.DEBUG) 
log_authlib.propagate = False # Ngăn chặn log được gửi tới root logger nếu không muốn bị trùng lặp

# Kích hoạt logging DEBUG cho thư viện HTTP underlying (urllib3) mà requests sử dụng
# Điều này cực kỳ hữu ích để xem chi tiết request headers, body và response
requests_log = logging.getLogger('requests.packages.urllib3')
requests_log.addHandler(handler)
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = False # Ngăn chặn trùng lặp

# Cấu hình root logger (tùy chọn nhưng hữu ích để bắt các log khác)
# Nếu bạn muốn tất cả các log khác cũng hiển thị DEBUG level
root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(logging.DEBUG)
# ----------------- Kết thúc phần Cấu hình Logging -----------------


# Tải biến môi trường từ file .env
load_dotenv()

# --- Khởi tạo các extension mà chưa liên kết với instance app ---
# Chúng ta khởi tạo chúng ở đây để chúng có thể được import và sử dụng ở các module khác
# mà không cần một instance Flask app cụ thể ngay lập tức.
migrate = Migrate()
jwt = JWTManager()
oauth = OAuth() # Rất quan trọng: Khởi tạo OAuth mà không truyền 'app' vào đây

# Hàm factory để tạo và cấu hình ứng dụng Flask
def create_app():
    """
    Tạo và cấu hình instance ứng dụng Flask.
    Tất cả logic khởi tạo và cấu hình ứng dụng sẽ nằm trong hàm này.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Tạo thư mục instance nếu chưa tồn tại
    os.makedirs(app.instance_path, exist_ok=True)

    # --- Cấu hình ứng dụng ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'dev-secret-change-me'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or 'jwt-secret-change-me'
    
    # Cấu hình Database
    default_sqlite_path = os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', f"sqlite:///{default_sqlite_path}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Cấu hình CORS (Cross-Origin Resource Sharing)
    CORS(app,
         resources={r"/api/*": {"origins": os.getenv("FRONTEND_ORIGIN", "*")}},
         supports_credentials=False) 

    # --- Liên kết các extensions với instance app đã được tạo ---
    # Bây giờ chúng ta gọi .init_app(app) để liên kết các extensions với 'app'
    db.init_app(app) # db được import từ models.py
    bcrypt.init_app(app) # bcrypt được import từ models.py
    migrate.init_app(app, db)
    jwt.init_app(app)
    oauth.init_app(app) # RẤT QUAN TRỌNG: Liên kết OAuth với app tại đây

    # Đăng ký Google OAuth client
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid profile email'},
    )
    
    # --- Đăng ký Blueprint ---
    # Import blueprint bên trong hàm factory để tránh lỗi import vòng tròn.
    # Khi auth.routes được import, nó sẽ truy cập 'oauth' đã được 'init_app' thành công.
    from auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Home route (ví dụ)
    @app.route('/')
    def index():
        return "Backend is running!"

    return app

if __name__ == '__main__':
    app = create_app() # Gọi hàm factory để tạo instance app

    # THÊM MỘT ROUTE TEST TẠM THỜI VÀO ĐÂY (Ngang hàng với app=create_app())
    @app.route('/test')
    def test_route():
        return "Route test works!"

    # ĐOẠN CODE DEBUG URL_MAP NẰM Ở ĐÂY (Ngang hàng với app=create_app())
    with app.app_context():
        print("\n===== Registered Routes =====")
        for rule in app.url_map.iter_rules():
            # Lọc ra các endpoint không mong muốn (ví dụ: static files) để dễ đọc hơn
            if rule.endpoint not in ['static']:
                print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, Rule: {rule.rule}")
        print("=============================\n")

    # THÊM use_reloader=False để đảm bảo print hiển thị rõ ràng

    app.run(debug=os.getenv('FLASK_DEBUG', '0') == '1', port=5000, use_reloader=False) 