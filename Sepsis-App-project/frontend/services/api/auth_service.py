from .api_client import ApiClient
from .api_urls import get_auth_urls

class AuthService:
    def __init__(self):
        self.client = ApiClient()  # client chung cho toàn hệ thống
        self.urls = get_auth_urls()  # load nhóm endpoint Auth

    def login(self, username: str, password: str):
        """Gọi API đăng nhập"""
        payload = {"username": username, "password": password}
        return self.client.post(self.urls["login"], json=payload)

    def register(self, username: str, password: str, email: str):
        """Gọi API đăng ký"""
        payload = {"username": username, "password": password, "email": email}
        return self.client.post(self.urls["register"], json=payload)

    def logout(self):
        """Gọi API đăng xuất"""
        return self.client.post(self.urls["logout"])

    def refresh_token(self, refresh_token: str):
        """Lấy access token mới bằng refresh token"""
        payload = {"refresh_token": refresh_token}
        return self.client.post(self.urls["refresh_token"], json=payload)
