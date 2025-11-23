"""Unit tests for Patient CRUD operations"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.crud import patient as patient_crud
from app.schemas.patient import PatientCreate, PatientUpdate


# Setup test database (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_patient(db):
    """Test tạo bệnh nhân mới"""
    patient_data = PatientCreate(
        patient_id="BN001",
        full_name="Nguyen Van A",
        gender="Nam",
        phone="0123456789"
    )
    
    patient = patient_crud.create_patient(db, patient_data)
    
    assert patient.patient_id == "BN001"
    assert patient.full_name == "Nguyen Van A"
    assert patient.gender == "Nam"


def test_get_patient(db):
    """Test lấy thông tin bệnh nhân"""
    # Tạo patient trước
    patient_data = PatientCreate(
        patient_id="BN002",
        full_name="Tran Thi B",
        gender="Nữ"
    )
    patient_crud.create_patient(db, patient_data)
    
    # Lấy patient
    patient = patient_crud.get_patient(db, "BN002")
    
    assert patient is not None
    assert patient.patient_id == "BN002"
    assert patient.full_name == "Tran Thi B"


def test_update_patient(db):
    """Test cập nhật thông tin bệnh nhân"""
    # Tạo patient
    patient_data = PatientCreate(
        patient_id="BN003",
        full_name="Le Van C",
        phone="0111111111"
    )
    patient_crud.create_patient(db, patient_data)
    
    # Update
    update_data = PatientUpdate(phone="0999999999")
    updated = patient_crud.update_patient(db, "BN003", update_data)
    
    assert updated.phone == "0999999999"
    assert updated.full_name == "Le Van C"  # Không thay đổi


def test_delete_patient(db):
    """Test xóa bệnh nhân"""
    # Tạo patient
    patient_data = PatientCreate(
        patient_id="BN004",
        full_name="Pham Thi D"
    )
    patient_crud.create_patient(db, patient_data)
    
    # Xóa
    result = patient_crud.delete_patient(db, "BN004")
    assert result is True
    
    # Kiểm tra đã xóa
    patient = patient_crud.get_patient(db, "BN004")
    assert patient is None


def test_search_patients(db):
    """Test tìm kiếm bệnh nhân"""
    # Tạo nhiều patients
    patients_data = [
        PatientCreate(patient_id="BN005", full_name="Nguyen Van E"),
        PatientCreate(patient_id="BN006", full_name="Nguyen Thi F"),
        PatientCreate(patient_id="BN007", full_name="Tran Van G"),
    ]
    
    for p in patients_data:
        patient_crud.create_patient(db, p)
    
    # Tìm kiếm "Nguyen"
    results = patient_crud.search_patients(db, "Nguyen")
    
    assert len(results) == 2
    assert all("Nguyen" in p.full_name for p in results)
