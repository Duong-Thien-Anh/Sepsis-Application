from .api_client import APIClient
from .api_urls import API_ROUTES

class AuthService:
    def __init__(self):
        self.auth_client = APIClient()
        self.urls = API_ROUTES["auth"]

    def login(self ,username: str , passsword: str):
        payload = {
            "username": username,
            "password": passsword
        } 

        response = self.client.post("/auth/login", json=payload)

        if response.get("status") == 200:
            token = response.get("data", {}).get("at")
            if token:
                self.client.set_token(token)
            return "success", response.get("data")
        else:
            return "error", response.get("message", "Đăng nhập thất bại!")
        
    def logout(self):
        self.client.clear_token()
        return "success", "Đã đăng xuất thành công."
    
    def google_login(self):
        response = self.client.post("/auth/google/login")
        return response
    
auth_service = AuthService()


