import requests
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env.frontend
def load_environment():
    load_dotenv(dotenv_path=".env.frontend")
    API_URL = os.getenv("API_URL", "http://localhost:8000")  # API backend