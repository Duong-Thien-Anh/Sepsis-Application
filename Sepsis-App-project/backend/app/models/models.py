"""SQLAlchemy ORM Models for FastAPI"""
from sqlalchemy import Column, String, Integer, Date, DateTime, Text, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

# Bảng tài khoản người dùng
class Account(Base):
    __tablename__ = 'Account'
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255))
    full_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(20))
    role = Column(String(50))
    status = Column(String(50))
    created_date = Column(Date)
    last_login = Column(DateTime)
    note = Column(Text)
    is_2fa_enabled = Column(Boolean, default=False)
    last_login_ip = Column(String(100))
    login_method = Column(String(50))

# Bảng nhân viên
class Employee(Base):
    __tablename__ = 'Employee'
    employee_id = Column(String(20), primary_key=True)
    full_name = Column(String(255))
    date_of_birth = Column(Date)
    gender = Column(String(10))
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    position = Column(String(100))
    department = Column(String(100))
    start_date = Column(Date)
    salary = Column(Numeric(15,2))
    education_level = Column(String(100))
    license_number = Column(String(100))
    emergency_contact_name = Column(String(255))
    emergency_contact_relation = Column(String(50))
    emergency_contact_phone = Column(String(20))
    photo_path = Column(String(255))
    username_account = Column(String(100), ForeignKey('Account.username'), unique=True)

    account = relationship('Account', backref='employee')

# Bảng bệnh nhân (Updated to match SQL schema)
class Patient(Base):
    __tablename__ = 'Patient'
    
    patient_id = Column(String(20), primary_key=True)
    full_name = Column(String(255), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String(10))
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    blood_type = Column(String(10))
    height_cm = Column(Integer)
    weight_kg = Column(Numeric(5,2))
    medical_history = Column(Text)
    emergency_contact_name = Column(String(255))
    emergency_contact_relation = Column(String(50))
    emergency_contact_phone = Column(String(20))
    photo_path = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Bảng hồ sơ bệnh án
class MedicalHistoryRecord(Base):
    __tablename__ = 'MedicalHistoryRecord'
    record_id = Column(String(20), primary_key=True)
    record_date = Column(Date)
    record_type = Column(String(100))
    description = Column(Text)
    patient_id = Column(String(20), ForeignKey('Patient.patient_id'), nullable=False)
    employee_id = Column(String(20), ForeignKey('Employee.employee_id'), nullable=False)

    patient = relationship('Patient', backref='medical_records')
    employee = relationship('Employee', backref='medical_records')

# Bảng chẩn đoán
class Diagnosis(Base):
    __tablename__ = 'Diagnosis'
    diagnosis_id = Column(String(20), primary_key=True)
    diagnosis_date = Column(Date)
    symptoms = Column(Text)
    diagnosis_result = Column(Text)
    diagnosis_name = Column(String(255))
    note = Column(Text)
    record_id = Column(String(20), ForeignKey('MedicalHistoryRecord.record_id'), nullable=False)

    record = relationship('MedicalHistoryRecord', backref='diagnoses')

# Bảng kết quả xét nghiệm
class TestResult(Base):
    __tablename__ = 'TestResult'
    result_id = Column(String(20), primary_key=True)
    test_type = Column(String(100))
    test_date = Column(Date)
    result = Column(Text)
    unit = Column(String(50))
    reference_range = Column(String(100))
    file_path = Column(String(255))
    note = Column(Text)
    record_id = Column(String(20), ForeignKey('MedicalHistoryRecord.record_id'), nullable=False)

    record = relationship('MedicalHistoryRecord', backref='test_results')

# Bảng kết quả AI
class AIResult(Base):
    __tablename__ = 'AIResult'
    ai_result_id = Column(String(20), primary_key=True)
    prediction_time = Column(DateTime)
    risk_score = Column(Numeric(5,2))
    sepsis_probability = Column(Numeric(5,2))
    suggested_treatment = Column(Text)
    ai_evaluation_result = Column(String(255))
    ai_model_explanation = Column(Text)
    diagnosis_id = Column(String(20), ForeignKey('Diagnosis.diagnosis_id'), unique=True, nullable=False)

    diagnosis = relationship('Diagnosis', backref='ai_result')

# Bảng lịch hẹn tái khám
class RecallAppointment(Base):
    __tablename__ = 'RecallAppointment'
    appointment_id = Column(String(20), primary_key=True)
    appointment_datetime = Column(DateTime)
    message_content = Column(Text)
    email_status = Column(String(50))
    note = Column(Text)
    patient_id = Column(String(20), ForeignKey('Patient.patient_id'), nullable=False)
    employee_id = Column(String(20), ForeignKey('Employee.employee_id'), nullable=False)

    patient = relationship('Patient', backref='appointments')
    employee = relationship('Employee', backref='appointments')

# Bảng log hoạt động
class ActivityLog(Base):
    __tablename__ = 'ActivityLog'
    log_id = Column(String(20), primary_key=True)
    timestamp = Column(DateTime)
    activity_type = Column(String(100))
    description = Column(Text)
    ip_address = Column(String(50))
    affected_object_type = Column(String(100))
    affected_object_id = Column(String(20))
    username_account = Column(String(100), ForeignKey('Account.username'), nullable=False)

    account = relationship('Account', backref='activity_logs')
