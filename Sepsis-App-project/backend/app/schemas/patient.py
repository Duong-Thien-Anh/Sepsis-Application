"""Pydantic schemas for Patient validation"""
from pydantic import BaseModel, EmailStr, validator, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


class PatientBase(BaseModel):
    """Schema cơ bản cho Patient"""
    full_name: str = Field(..., min_length=1, max_length=255, description="Họ và tên bệnh nhân")
    date_of_birth: Optional[date] = Field(None, description="Ngày sinh")
    gender: Optional[str] = Field(None, max_length=10, description="Giới tính")
    phone: Optional[str] = Field(None, max_length=20, description="Số điện thoại")
    email: Optional[EmailStr] = Field(None, description="Email")
    address: Optional[str] = Field(None, description="Địa chỉ")
    blood_type: Optional[str] = Field(None, max_length=10, description="Nhóm máu")
    height_cm: Optional[int] = Field(None, ge=0, le=300, description="Chiều cao (cm)")
    weight_kg: Optional[Decimal] = Field(None, ge=0, le=500, description="Cân nặng (kg)")
    medical_history: Optional[str] = Field(None, description="Tiền sử bệnh")
    emergency_contact_name: Optional[str] = Field(None, max_length=255, description="Tên người liên hệ khẩn cấp")
    emergency_contact_relation: Optional[str] = Field(None, max_length=50, description="Quan hệ")
    emergency_contact_phone: Optional[str] = Field(None, max_length=20, description="SĐT khẩn cấp")
    photo_path: Optional[str] = Field(None, max_length=255, description="Đường dẫn ảnh")
    
    @validator('gender')
    def validate_gender(cls, v):
        """Validate gender"""
        if v and v not in ['Nam', 'Nữ', 'Khác']:
            raise ValueError('Giới tính phải là: Nam, Nữ, hoặc Khác')
        return v
    
    @validator('blood_type')
    def validate_blood_type(cls, v):
        """Validate blood type"""
        valid_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if v and v not in valid_types:
            raise ValueError(f'Nhóm máu không hợp lệ. Phải là một trong: {", ".join(valid_types)}')
        return v


class PatientCreate(PatientBase):
    """Schema khi tạo Patient mới"""
    patient_id: str = Field(..., min_length=1, max_length=20, description="Mã bệnh nhân")
    
    @validator('patient_id')
    def validate_patient_id(cls, v):
        """Validate patient ID format"""
        if not v.startswith('BN'):
            raise ValueError('Mã bệnh nhân phải bắt đầu bằng "BN"')
        return v


class PatientUpdate(PatientBase):
    """Schema khi update Patient (tất cả fields optional)"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)


class Patient(PatientBase):
    """Schema response (bao gồm cả timestamps và computed fields)"""
    patient_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    age: Optional[int] = None  # Computed field
    
    class Config:
        orm_mode = True  # Cho phép convert từ ORM object
        from_attributes = True  # Pydantic v2


class PatientSearchRequest(BaseModel):
    """Schema cho request tìm kiếm bệnh nhân"""
    patient_id: str = Field(..., description="Mã bệnh nhân cần tìm")


class PatientListResponse(BaseModel):
    """Schema cho response danh sách bệnh nhân (có pagination)"""
    patients: list[Patient]
    total: int
    pages: int
    current_page: int
