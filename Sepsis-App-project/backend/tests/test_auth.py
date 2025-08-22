from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pytest
from fastapi.testclient import TestClient

app = FastAPI()

# Dữ liệu mẫu để kiểm tra đăng nhập
fake_users_db = {
    "admin": "12345678"
}

# Schema cho request body
class LoginRequest(BaseModel):
    username: str
    password: str

# API kiểm tra đăng nhập
@app.post("/auth/login")
def login(request: LoginRequest):
    username = request.username
    password = request.password

    # Kiểm tra thông tin đăng nhập
    if username in fake_users_db and fake_users_db[username] == password:
        return {"access_token": "fake-jwt-token", "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail():
    response = client.post("/auth/login", json={
        "username": "wrong",
        "password": "wrong"
    })
    assert response.status_code == 401

# Chạy server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
