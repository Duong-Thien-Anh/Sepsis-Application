import requests
from services.api.api_urls import BASE_URL
class APIClient:
    def __init__(self):
        # Lấy base_url từ file config tập trung
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.token = None


    def set_token(self, token: str):
        """Gắn token sau khi login và cập nhật vào session header."""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self):
        """Xóa token khi logout."""
        self.token = None
        self.session.headers.pop("Authorization", None)

    def request(self, method, endpoint, **kwargs):
        """Hàm gọi API chung, chỉ cần định nghĩa một lần."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Nên ném ra lỗi để lớp cao hơn xử lý thay vì trả về dict
            raise ConnectionError(f"API request failed: {e}") from e