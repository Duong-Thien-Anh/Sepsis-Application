import requests

class APIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def set_token(self, token: str):
        """Gắn token sau khi login"""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def request(self, method, endpoint, **kwargs):
        """Hàm gọi API chung"""
        url = f"{self.base_url}{endpoint}"
        self.token = None

    def set_token(self, token: str):
        """Gắn token sau khi login"""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def request(self, method, endpoint, **kwargs):
        """Hàm gọi API chung"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
