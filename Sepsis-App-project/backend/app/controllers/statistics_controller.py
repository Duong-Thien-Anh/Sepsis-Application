# app/controllers/statistics_controller.py
from app.services.statistics_service import get_gender_stats, get_age_group_stats

def get_gender_statistics():
    data = get_gender_stats()
    return {"success": True, "data": data}

def get_age_group_statistics():
    data = get_age_group_stats()
    return {"success": True, "data": data}

