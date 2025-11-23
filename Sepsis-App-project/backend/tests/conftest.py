"""
Pytest Configuration & Fixtures
Chứa các setup dùng chung cho tất cả test files
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.models import Base
from app.db.session import get_db

# Tạo in-memory SQLite database cho testing (không ảnh hưởng MySQL thật)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Tạo database mới cho mỗi test
    Sau khi test xong sẽ xóa hết dữ liệu
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    TestClient để gọi API
    Override database dependency để dùng test database
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_patient_data():
    """
    Dữ liệu patient mẫu để dùng trong tests
    """
    return {
        "patient_id": "BN001",
        "full_name": "Nguyễn Văn A",
        "gender": "Nam",
        "date_of_birth": "1990-01-15",
        "phone_number": "0912345678",
        "email": "nguyenvana@example.com",
        "address": "123 Đường ABC, Quận 1, TP.HCM",
        "blood_type": "O+"
    }
