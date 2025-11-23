"""CRUD operations for Patient"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from datetime import datetime
from typing import Optional


def get_patients(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    gender: Optional[str] = None
) -> list[Patient]:
    """
    Lấy danh sách bệnh nhân với pagination và filter
    
    Args:
        db: Database session
        skip: Số record bỏ qua
        limit: Số record tối đa
        search: Từ khóa tìm kiếm theo tên
        gender: Lọc theo giới tính
    
    Returns:
        List of Patient objects
    """
    query = db.query(Patient)
    
    # Filter theo giới tính
    if gender:
        query = query.filter(Patient.gender == gender)
    
    # Search theo tên
    if search:
        query = query.filter(Patient.full_name.ilike(f"%{search}%"))
    
    return query.offset(skip).limit(limit).all()


def get_patients_count(
    db: Session,
    search: Optional[str] = None,
    gender: Optional[str] = None
) -> int:
    """Đếm tổng số bệnh nhân (cho pagination)"""
    query = db.query(func.count(Patient.patient_id))
    
    if gender:
        query = query.filter(Patient.gender == gender)
    
    if search:
        query = query.filter(Patient.full_name.ilike(f"%{search}%"))
    
    return query.scalar()


def get_patient(db: Session, patient_id: str) -> Optional[Patient]:
    """
    Lấy thông tin 1 bệnh nhân theo ID
    
    Args:
        db: Database session
        patient_id: Mã bệnh nhân
    
    Returns:
        Patient object hoặc None nếu không tìm thấy
    """
    return db.query(Patient).filter(Patient.patient_id == patient_id).first()


def create_patient(db: Session, patient: PatientCreate) -> Patient:
    """
    Tạo bệnh nhân mới
    
    Args:
        db: Database session
        patient: PatientCreate schema
    
    Returns:
        Patient object đã tạo
    """
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(
    db: Session,
    patient_id: str,
    patient_data: PatientUpdate
) -> Optional[Patient]:
    """
    Cập nhật thông tin bệnh nhân
    
    Args:
        db: Database session
        patient_id: Mã bệnh nhân
        patient_data: PatientUpdate schema
    
    Returns:
        Patient object đã update hoặc None nếu không tìm thấy
    """
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    
    # Chỉ update các field không None
    update_data = patient_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_patient, field, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: str) -> bool:
    """
    Xóa bệnh nhân
    
    Args:
        db: Database session
        patient_id: Mã bệnh nhân
    
    Returns:
        True nếu xóa thành công, False nếu không tìm thấy
    """
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return False
    
    db.delete(db_patient)
    db.commit()
    return True


def search_patients(db: Session, keyword: str) -> list[Patient]:
    """
    Tìm kiếm bệnh nhân theo từ khóa
    
    Args:
        db: Database session
        keyword: Từ khóa tìm kiếm
    
    Returns:
        List of Patient objects
    """
    return db.query(Patient).filter(
        Patient.full_name.ilike(f"%{keyword}%")
    ).all()


def get_patients_by_age_range(
    db: Session,
    min_age: int,
    max_age: int
) -> list[Patient]:
    """
    Lọc bệnh nhân theo độ tuổi
    
    Args:
        db: Database session
        min_age: Tuổi tối thiểu
        max_age: Tuổi tối đa
    
    Returns:
        List of Patient objects
    """
    from datetime import timedelta
    today = datetime.now()
    max_birth = today - timedelta(days=min_age * 365)
    min_birth = today - timedelta(days=max_age * 365)
    
    return db.query(Patient).filter(
        Patient.date_of_birth.between(min_birth, max_birth)
    ).all()
