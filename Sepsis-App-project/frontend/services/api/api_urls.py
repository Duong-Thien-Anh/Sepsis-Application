BASE_URL = "http://127.0.0.1:5000"
# -------------------------------
# Auth APIs
# -------------------------------
def get_auth_urls():
    return {
        # Thêm "/api" vào đây
        "login": "/api/auth/login",
        "register": "/api/auth/register",
        "logout": "/api/auth/logout",
        "refresh_token": "/api/auth/refresh",
    }


# -------------------------------
# User APIs
# -------------------------------
def get_user_urls():
    return {
        "get_user": f"{BASE_URL}/users/me",
        "update_user": f"{BASE_URL}/users/update",
        "change_password": f"{BASE_URL}/users/change-password",
    }


# -------------------------------
# Patient APIs
# -------------------------------
def get_patient_urls():
    return {
        "list_patients": f"{BASE_URL}/patients",
        "create_patient": f"{BASE_URL}/patients/create",
        "update_patient": f"{BASE_URL}/patients/update",
        "delete_patient": f"{BASE_URL}/patients/delete",
    }


# -------------------------------
# Report APIs
# -------------------------------
def get_report_urls():
    return {
        "list_reports": f"{BASE_URL}/reports",
        "export_report": f"{BASE_URL}/reports/export",
        "statistics": f"{BASE_URL}/reports/statistics",
    }
