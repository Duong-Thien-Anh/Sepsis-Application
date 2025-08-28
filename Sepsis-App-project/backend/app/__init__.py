# backend/app/__init__.py
import os
import logging
import sys
from flask import Flask
from .extensions import db, bcrypt, migrate, jwt, oauth
from datetime import timedelta

def setup_logging():
    """Cấu hình logging chi tiết cho ứng dụng."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

def create_app():
    """Hàm factory để tạo và cấu hình ứng dụng Flask."""
    setup_logging() # Gọi hàm cấu hình logging
    
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Cấu hình ứng dụng
    # SỬA LỖI: Dùng chung JWT_SECRET_KEY cho cả SECRET_KEY
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    app.config['SECRET_KEY'] = jwt_secret
    app.config['JWT_SECRET_KEY'] = jwt_secret
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Cập nhật: Kéo dài thời gian hết hạn của token
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) # Mặc định là 15 phút
    # Liên kết các extensions với app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    oauth.init_app(app)

    # Đăng ký Google OAuth client
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid profile email'},
    )
    
    with app.app_context():
        from .models import models
        from .routes import register_routes
        register_routes(app)

    return app
