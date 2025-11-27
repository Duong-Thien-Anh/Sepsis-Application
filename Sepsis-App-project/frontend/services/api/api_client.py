import requests

class APIClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def set_token(self, token: str):
        """Gắn token sau khi login"""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        print(f"✓ Token đã được set: {token[:20]}...")

    def clear_token(self):
        self.token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
        print("✓ Token đã được xóa.")

    def request(self, method, endpoint, **kwargs):
        """Hàm gọi API chung"""
        url = f"{self.base_url}{endpoint}"
        try:
            # Gửi request
            response = self.session.request(method, url, **kwargs)
            
            # Raise exception nếu status code 4xx hoặc 5xx
            response.raise_for_status()
            
            # Parse JSON và trả về
            return response.json()
        
        except requests.exceptions.Timeout:
            # Timeout: Server không phản hồi đúng thời gian
            return {
                "status": 408,
                "message": "Timeout: Không thể kết nối tới server",
                "data": None
            }
        
        except requests.exceptions.ConnectionError:
            # Connection Error: Server không chạy hoặc mất mạng
            return {
                "status": 503,
                "message": "Không thể kết nối Backend. Vui lòng kiểm tra server!",
                "data": None
            }
        
        except requests.exceptions.HTTPError:
            # HTTP Error: Server trả về 4xx, 5xx
            try:
                # Backend có thể trả về JSON error
                return response.json()
            except:
                return {
                    "status": response.status_code,
                    "message": f"HTTP Error {response.status_code}",
                    "data": None
                }
        
        except Exception as e:
            # Các lỗi khác không xác định
            return {
                "status": 500,
                "message": f"Lỗi không xác định: {str(e)}",
                "data": None
            }
        
    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)
