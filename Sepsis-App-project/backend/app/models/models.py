from .database import db

# Bảng tài khoản người dùng
class Account(db.Model):
    __tablename__ = 'Account'
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50))
    status = db.Column(db.String(50))
    created_date = db.Column(db.Date)
    last_login = db.Column(db.DateTime)
    note = db.Column(db.Text)
    is_2fa_enabled = db.Column(db.Boolean, default=False)
    last_login_ip = db.Column(db.String(100))
    login_method = db.Column(db.String(50))

# Bảng nhân viên
class Employee(db.Model):
    __tablename__ = 'Employee'
    employee_id = db.Column(db.String(20), primary_key=True)
    full_name = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    address = db.Column(db.Text)
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    salary = db.Column(db.Numeric(15,2))
    education_level = db.Column(db.String(100))
    license_number = db.Column(db.String(100))
    emergency_contact_name = db.Column(db.String(255))
    emergency_contact_relation = db.Column(db.String(50))
    emergency_contact_phone = db.Column(db.String(20))
    photo_path = db.Column(db.String(255))
    username_account = db.Column(db.String(100), db.ForeignKey('Account.username'), unique=True)

    account = db.relationship('Account', backref='employee')

# Bảng bệnh nhân (Updated to match SQL schema)
class Patient(db.Model):
    __tablename__ = 'Patient'
    
    patient_id = db.Column(db.String(20), primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    address = db.Column(db.Text)
    blood_type = db.Column(db.String(10))
    height_cm = db.Column(db.Integer)
    weight_kg = db.Column(db.Numeric(5,2))
    medical_history = db.Column(db.Text)
    emergency_contact_name = db.Column(db.String(255))
    emergency_contact_relation = db.Column(db.String(50))
    emergency_contact_phone = db.Column(db.String(20))
    photo_path = db.Column(db.String(255))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())

    def to_dict(self):
        """Convert model to dictionary for API response"""
        return {
            'patient_id': self.patient_id,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'blood_type': self.blood_type,
            'height_cm': self.height_cm,
            'weight_kg': float(self.weight_kg) if self.weight_kg else None,
            'medical_history': self.medical_history,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_relation': self.emergency_contact_relation,
            'emergency_contact_phone': self.emergency_contact_phone,
            'photo_path': self.photo_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Bảng hồ sơ bệnh án
class MedicalHistoryRecord(db.Model):
    __tablename__ = 'MedicalHistoryRecord'
    record_id = db.Column(db.String(20), primary_key=True)
    record_date = db.Column(db.Date)
    record_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    patient_id = db.Column(db.String(20), db.ForeignKey('Patient.patient_id'), nullable=False)
    employee_id = db.Column(db.String(20), db.ForeignKey('Employee.employee_id'), nullable=False)

    patient = db.relationship('Patient', backref='medical_records')
    employee = db.relationship('Employee', backref='medical_records')

# Bảng chẩn đoán
class Diagnosis(db.Model):
    __tablename__ = 'Diagnosis'
    diagnosis_id = db.Column(db.String(20), primary_key=True)
    diagnosis_date = db.Column(db.Date)
    symptoms = db.Column(db.Text)
    diagnosis_result = db.Column(db.Text)
    diagnosis_name = db.Column(db.String(255))
    note = db.Column(db.Text)
    record_id = db.Column(db.String(20), db.ForeignKey('MedicalHistoryRecord.record_id'), nullable=False)

    record = db.relationship('MedicalHistoryRecord', backref='diagnoses')

# Bảng kết quả xét nghiệm
class TestResult(db.Model):
    __tablename__ = 'TestResult'
    result_id = db.Column(db.String(20), primary_key=True)
    test_type = db.Column(db.String(100))
    test_date = db.Column(db.Date)
    result = db.Column(db.Text)
    unit = db.Column(db.String(50))
    reference_range = db.Column(db.String(100))
    file_path = db.Column(db.String(255))
    note = db.Column(db.Text)
    record_id = db.Column(db.String(20), db.ForeignKey('MedicalHistoryRecord.record_id'), nullable=False)

    record = db.relationship('MedicalHistoryRecord', backref='test_results')

# Bảng kết quả AI
class AIResult(db.Model):
    __tablename__ = 'AIResult'
    ai_result_id = db.Column(db.String(20), primary_key=True)
    prediction_time = db.Column(db.DateTime)
    risk_score = db.Column(db.Numeric(5,2))
    sepsis_probability = db.Column(db.Numeric(5,2))
    suggested_treatment = db.Column(db.Text)
    ai_evaluation_result = db.Column(db.String(255))
    ai_model_explanation = db.Column(db.Text)
    diagnosis_id = db.Column(db.String(20), db.ForeignKey('Diagnosis.diagnosis_id'), unique=True, nullable=False)

    diagnosis = db.relationship('Diagnosis', backref='ai_result')

# Bảng lịch hẹn tái khám
class RecallAppointment(db.Model):
    __tablename__ = 'RecallAppointment'
    appointment_id = db.Column(db.String(20), primary_key=True)
    appointment_datetime = db.Column(db.DateTime)
    message_content = db.Column(db.Text)
    email_status = db.Column(db.String(50))
    note = db.Column(db.Text)
    patient_id = db.Column(db.String(20), db.ForeignKey('Patient.patient_id'), nullable=False)
    employee_id = db.Column(db.String(20), db.ForeignKey('Employee.employee_id'), nullable=False)

    patient = db.relationship('Patient', backref='appointments')
    employee = db.relationship('Employee', backref='appointments')

# Bảng log hoạt động
class ActivityLog(db.Model):
    __tablename__ = 'ActivityLog'
    log_id = db.Column(db.String(20), primary_key=True)
    timestamp = db.Column(db.DateTime)
    activity_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    affected_object_type = db.Column(db.String(100))
    affected_object_id = db.Column(db.String(20))
    username_account = db.Column(db.String(100), db.ForeignKey('Account.username'), nullable=False)

    account = db.relationship('Account', backref='activity_logs')