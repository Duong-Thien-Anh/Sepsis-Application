# Base URL của backend
BASE_URL = "http://localhost:5000/api"

API_ROUTES = {
    # -------------------------------
    # Auth APIs
    # -------------------------------
    "auth": {
        "login": f"{BASE_URL}/auth/login",
        "register": f"{BASE_URL}/auth/register",
        "logout": f"{BASE_URL}/auth/logout",
        "refresh_token": f"{BASE_URL}/auth/refresh",
    },

    # -------------------------------
    # User APIs
    # -------------------------------
    "user": {
        "get_user": f"{BASE_URL}/users/me",
        "update_user": f"{BASE_URL}/users/update",
        "change_password": f"{BASE_URL}/users/change-password",
    },

    # -------------------------------
    # Patient APIs
    # -------------------------------
    "patient": {
        "list": f"{BASE_URL}/patients",
        "create": f"{BASE_URL}/patients/create",
        "update": f"{BASE_URL}/patients/update",
        "delete": f"{BASE_URL}/patients/delete",
    },

    # -------------------------------
    # Report APIs
    # -------------------------------
    "report": {
        "list": f"{BASE_URL}/reports",
        "export": f"{BASE_URL}/reports/export",
        "statistics": f"{BASE_URL}/reports/statistics",
    }
}
