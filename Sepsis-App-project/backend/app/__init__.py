# backend/app/__init__.py
import os
from flask import Flask
from dotenv import load_dotenv
# Sửa lỗi: Import từ extensions.py
from .extensions import db, bcrypt, migrate, jwt, oauth

load_dotenv()

def create_app():
    """Hàm factory để tạo và cấu hình ứng dụng Flask."""
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Cấu hình ứng dụng
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
