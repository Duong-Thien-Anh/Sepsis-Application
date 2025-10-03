from ..models.models import Patient, Employee, db
from datetime import datetime
from ..models.models import Patient

def find_patient_by_id(patient_id):
    """Tìm bệnh nhân theo ID"""
    patient = Patient.query.get(patient_id)
    if not patient:
        return None
    return serialize_patient(patient)

def save_or_update_patient(data):
    """Thêm mới hoặc cập nhật thông tin bệnh nhân"""
    patient_id = data.get("patient_id")
    patient = Patient.query.get(patient_id)
    if patient:
        # Cập nhật
        for key, value in data.items():
            if hasattr(patient, key) and value is not None:
                setattr(patient, key, value)
        db.session.commit()
        return "updated"
    else:
        # Tạo mới
        new_patient = Patient(
            patient_id=data.get("patient_id"),
            full_name=data.get("full_name"),
            date_of_birth=datetime.strptime(data.get("date_of_birth"), "%Y-%m-%d").date() if data.get("date_of_birth") else None,
            gender=data.get("gender"),
            diagnosis=data.get("diagnosis"),
            admission_date=datetime.strptime(data.get("admission_date"), "%Y-%m-%d").date() if data.get("admission_date") else None,
            attending_doctor_id=data.get("attending_doctor_id")
        )
        db.session.add(new_patient)
        db.session.commit()
        return "created"

def serialize_patient(p):
    """Chuyển đối tượng Patient thành dict"""
    doctor_name = None
    if p.attending_doctor_id:
        doctor = Employee.query.get(p.attending_doctor_id)
        doctor_name = doctor.full_name if doctor else None

    age = None
    if p.date_of_birth:
        age = datetime.now().year - p.date_of_birth.year

    return {
        "patient_id": p.patient_id,
        "full_name": p.full_name,
        "age": age,
        "gender": p.gender,
        "diagnosis": p.diagnosis,
        "admission_date": p.admission_date.strftime("%Y-%m-%d") if p.admission_date else None,
        "attending_doctor": doctor_name
    }

def get_patient_list(page, per_page, search, gender):
    query = Patient.query

    # Filter theo giới tính
    if gender:
        query = query.filter(Patient.gender == gender)

    # Search theo tên
    if search:
        query = query.filter(Patient.full_name.ilike(f"%{search}%"))

    # Pagination
    patients = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "patients": [patient.to_dict() for patient in patients.items],
        "total": patients.total,
        "pages": patients.pages,
        "current_page": patients.page
    }

def get_patient_by_id(patient_id):
    patient = Patient.query.get(patient_id)
    return patient.to_dict() if patient else None

def delete_patient_by_id(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return False
    db.session.delete(patient)
    db.session.commit()
    return True
