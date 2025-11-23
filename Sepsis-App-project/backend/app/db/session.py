"""Database session configuration for FastAPI with MySQL"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ========================================
# MYSQL CONNECTION CONFIGURATION
# ========================================
# Cấu hình kết nối MySQL
MYSQL_USER = os.getenv("MYSQL_USER", "root")           # Username MySQL
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "matkhau")       # Password MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")      # Host (localhost hoặc IP)
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")           # Port MySQL (mặc định: 3306)
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "sepsis_application")  # Tên database

# Tạo connection string cho MySQL
# Format: mysql+pymysql://username:password@host:port/database
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

print(f"🔌 Connecting to MySQL: {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")

# Tạo engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,      # Kiểm tra connection trước khi dùng
    pool_recycle=3600,       # Recycle connection sau 1 giờ
    echo=False,              # Set True để debug SQL queries
    pool_size=10,            # Số connection trong pool
    max_overflow=20          # Số connection tối đa khi pool đầy
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho models
Base = declarative_base()

# Dependency để lấy DB session
def get_db():
    """
    Dependency injection cho database session.
    Sử dụng: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
