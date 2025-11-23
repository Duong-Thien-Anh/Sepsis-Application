"""Patient API routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import math

from app.db.session import get_db
from app.crud import patient as patient_crud
from app.schemas.patient import (
    Patient,
    PatientCreate,
    PatientUpdate,
    PatientSearchRequest,
    PatientListResponse
)
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=PatientListResponse)
def get_all_patients(
    page: int = Query(1, ge=1, description="Số trang"),
    per_page: int = Query(10, ge=1, le=100, description="Số record mỗi trang"),
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên"),
    gender: Optional[str] = Query(None, description="Lọc theo giới tính"),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách tất cả bệnh nhân (có pagination)
    
    - **page**: Số trang (mặc định: 1)
    - **per_page**: Số record mỗi trang (mặc định: 10, max: 100)
    - **search**: Tìm kiếm theo tên bệnh nhân
    - **gender**: Lọc theo giới tính (Nam/Nữ/Khác)
    """
    skip = (page - 1) * per_page
    
    # Lấy danh sách bệnh nhân
    patients = patient_crud.get_patients(
        db,
        skip=skip,
        limit=per_page,
        search=search,
        gender=gender
    )
    
    # Đếm tổng số
    total = patient_crud.get_patients_count(db, search=search, gender=gender)
    pages = math.ceil(total / per_page) if per_page > 0 else 0
    
    # Thêm computed field 'age'
    for patient in patients:
        if patient.date_of_birth:
            patient.age = datetime.now().year - patient.date_of_birth.year
    
    return PatientListResponse(
        patients=patients,
        total=total,
        pages=pages,
        current_page=page
    )


@router.get("/{patient_id}", response_model=Patient)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    """
    Lấy thông tin chi tiết 1 bệnh nhân theo ID
    
    - **patient_id**: Mã bệnh nhân (VD: BN001)
    """
    patient = patient_crud.get_patient(db, patient_id=patient_id)
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy bệnh nhân với mã: {patient_id}"
        )
    
    # Thêm computed field 'age'
    if patient.date_of_birth:
        patient.age = datetime.now().year - patient.date_of_birth.year
    
    return patient


@router.post("/search", response_model=Patient)
def search_patient(
    request: PatientSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Tìm kiếm bệnh nhân theo mã
    
    - **patient_id**: Mã bệnh nhân cần tìm
    """
    patient = patient_crud.get_patient(db, patient_id=request.patient_id)
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy bệnh nhân"
        )
    
    # Thêm computed field 'age'
    if patient.date_of_birth:
        patient.age = datetime.now().year - patient.date_of_birth.year
    
    return patient


@router.post("/", response_model=Patient, status_code=201)
def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_db)
):
    """
    Tạo bệnh nhân mới
    
    - **patient_id**: Mã bệnh nhân (bắt đầu bằng BN)
    - **full_name**: Họ và tên (bắt buộc)
    - Các trường khác: optional
    """
    # Kiểm tra patient_id đã tồn tại chưa
    existing = patient_crud.get_patient(db, patient_id=patient_in.patient_id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Mã bệnh nhân {patient_in.patient_id} đã tồn tại"
        )
    
    patient = patient_crud.create_patient(db, patient=patient_in)
    return patient


@router.put("/{patient_id}", response_model=Patient)
def update_patient(
    patient_id: str,
    patient_in: PatientUpdate,
    db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin bệnh nhân
    
    - **patient_id**: Mã bệnh nhân cần cập nhật
    - Chỉ cần gửi các trường muốn update (partial update)
    """
    patient = patient_crud.get_patient(db, patient_id=patient_id)
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy bệnh nhân với mã: {patient_id}"
        )
    
    patient = patient_crud.update_patient(db, patient_id=patient_id, patient_data=patient_in)
    return patient


@router.delete("/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    """
    Xóa bệnh nhân
    
    - **patient_id**: Mã bệnh nhân cần xóa
    """
    success = patient_crud.delete_patient(db, patient_id=patient_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy bệnh nhân với mã: {patient_id}"
        )
    
    return {"message": "Xóa bệnh nhân thành công", "patient_id": patient_id}


@router.get("/search/by-keyword/", response_model=list[Patient])
def search_patients_by_keyword(
    keyword: str = Query(..., min_length=1, description="Từ khóa tìm kiếm"),
    db: Session = Depends(get_db)
):
    """
    Tìm kiếm bệnh nhân theo tên (không phân trang)
    
    - **keyword**: Từ khóa tìm kiếm trong tên bệnh nhân
    """
    patients = patient_crud.search_patients(db, keyword=keyword)
    
    # Thêm computed field 'age'
    for patient in patients:
        if patient.date_of_birth:
            patient.age = datetime.now().year - patient.date_of_birth.year
    
    return patients
