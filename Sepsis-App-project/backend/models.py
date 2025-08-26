# backend/app/models/models.py
from datetime import datetime
# Sửa lỗi: Import db, bcrypt từ app.extensions
from app.extensions import db, bcrypt

class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(db.Model, TimestampMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), unique=True, nullable=True)
    name = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin  = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, raw_password: str):
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")
    def check_password(self, raw_password: str):
        return bcrypt.check_password_hash(self.password_hash, raw_password) if self.password_hash else False
    def to_dict(self):
        return {
            'id': self.id, 'email': self.email, 'name': self.name,
            'profile_picture': self.profile_picture, 'is_active': self.is_active,
            'is_admin': self.is_admin, 'created_at': self.created_at.isoformat()
        }
