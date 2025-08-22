import os
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables
    """
    load_dotenv()
    return {
        "API_URL": os.getenv("API_URL", "http://localhost:8000"),
        "API_KEY": os.getenv("API_KEY", ""),
        "TIMEOUT": int(os.getenv("TIMEOUT", "10"))
    }

# Load config và export các biến
_config = load_environment()

# Export các biến để có thể import trực tiếp
API_URL = _config["API_URL"]
API_KEY = _config["API_KEY"] 
TIMEOUT = _config["TIMEOUT"]

# Export thêm hàm get config nếu cần
def get_config():
    return _config

def get_api_url():
    return API_URL
