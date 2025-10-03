from app.models.models import Patient
from app.models.database import db

def get_gender_stats():
    """Thống kê số lượng bệnh nhân theo giới tính"""
    result = db.session.query(Patient.gender, db.func.count(Patient.id)).group_by(Patient.gender).all()
    return {gender: count for gender, count in result}

def get_age_group_stats():
    """Thống kê số lượng bệnh nhân theo nhóm tuổi"""
    groups = {
        "<18": (0, 17),
        "18-35": (18, 35),
        "36-60": (36, 60),
        "61-80": (61, 80),
        ">80": (81, 200)
    }

    stats = {}
    for label, (low, high) in groups.items():
        count = db.session.query(db.func.count(Patient.id))\
                          .filter(Patient.age >= low, Patient.age <= high).scalar()
        stats[label] = count
    return stats
