# frontend/api/api_url.py

# -------------------------------
# Base URL của backend
# -------------------------------
BASE_URL = "http://localhost:5000/api"

API_ROUTES = {
    # -------------------------------
    # Auth APIs (Xác thực & quản lý tài khoản)
    # -------------------------------
    "auth": {
        "login": f"{BASE_URL}/auth/login",
        "signup": f"{BASE_URL}/auth/signup",
        "google_login": f"{BASE_URL}/auth/google/login",
        "google_callback": f"{BASE_URL}/auth/google/callback",
        "logout": f"{BASE_URL}/auth/logout",
        "refresh_token": f"{BASE_URL}/auth/refresh",
        "forgot_password": f"{BASE_URL}/auth/forgot-password",
        "reset_password": f"{BASE_URL}/auth/reset-password",
    },

    # -------------------------------
    # User APIs (Người dùng hệ thống)
    # -------------------------------
    "user": {
        "get_user": f"{BASE_URL}/users/me",
        "update_user": f"{BASE_URL}/users/update",
        "change_password": f"{BASE_URL}/users/change-password",
        "list_all": f"{BASE_URL}/users/list",
        "delete_user": f"{BASE_URL}/users/delete",
    },

    # -------------------------------
    # Patient APIs (Thông tin bệnh nhân)
    # -------------------------------
    "patient": {
        "list": f"{BASE_URL}/patients",
        "get_by_id": f"{BASE_URL}/patients/get",
        "create": f"{BASE_URL}/patients/create",
        "update": f"{BASE_URL}/patients/update",
        "delete": f"{BASE_URL}/patients/delete",
        "search": f"{BASE_URL}/patients/search",
    },

    # -------------------------------
    # Diagnosis APIs (Chẩn đoán & xét nghiệm)
    # -------------------------------
    "diagnosis": {
        "predict_sepsis": f"{BASE_URL}/diagnosis/predict",      # Gọi model ML để dự đoán nhiễm trùng máu
        "save_result": f"{BASE_URL}/diagnosis/save-result",     # Lưu kết quả chẩn đoán
        "get_history": f"{BASE_URL}/diagnosis/history",         # Lấy lịch sử xét nghiệm bệnh nhân
    },

    # -------------------------------
    # Report APIs (Báo cáo - thống kê)
    # -------------------------------
    "report": {
        "list": f"{BASE_URL}/reports",
        "export": f"{BASE_URL}/reports/export",
        "statistics": f"{BASE_URL}/reports/statistics",
    },

    # -------------------------------
    # Statistics APIs (Phục vụ form thống kê)
    # -------------------------------
    "statistics": {
        "gender": f"{BASE_URL}/statistics/gender",
        "age_group": f"{BASE_URL}/statistics/age-group",
        "month": f"{BASE_URL}/statistics/monthly",
        "doctor": f"{BASE_URL}/statistics/doctor",
    },
}
