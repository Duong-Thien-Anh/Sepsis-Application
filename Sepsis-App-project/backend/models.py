from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData

# Đặt naming convention để migrate/rollback ổn định
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
bcrypt = Bcrypt()

class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # Optional, only if using email/password authentication
    google_id = db.Column(db.String(255), unique=True, nullable=True)  # Google OAuth ID
    name = db.Column(db.String(255), nullable=True)  # User's name from Google
    profile_picture = db.Column(db.String(255), nullable=True)  # User's profile picture from Google

    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin  = db.Column(db.Boolean, nullable=False, default=False)
    
    # SỬA LỖI: Thêm lại hàm to_dict() bị thiếu
      # SỬA LỖI: Căn lề chính xác cho hàm to_dict()
    def to_dict(self):
        """Chuyển đổi object User thành dictionary để trả về JSON."""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'profile_picture': self.profile_picture,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }
    
    # Set password (used for email/password authentication)
    def set_password(self, raw_password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    # Check password (used for email/password authentication)
    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    # Tạo người dùng mới từ Google OAuth
    @classmethod
    def from_google(cls, google_id, name, email, profile_picture):
        return cls(google_id=google_id, name=name, email=email, profile_picture=profile_picture)

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
