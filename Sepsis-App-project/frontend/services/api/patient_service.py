from .api_client import APIClient
from .api_urls import API_ROUTES

class PatientService:
    def __init__(self):
        self.patient_client = APIClient()
        self.urls = API_ROUTES["patient"]

    def get_all_patients(self):
        try:
            reponse = APIClient.get(self.urls["list"])
            if reponse and reponse.get("status") == 200:
                return True, reponse.get("data", [])
            else:
                error_mgs = reponse.get("message", "Lấy danh sách bệnh nhân thất bại.") if reponse else "Không thể kết nối tới server."
                return False, error_mgs
        except Exception as e:
            return False, f"Lỗi không xác định: {str(e)}"
        
patient_service = PatientService()