from urllib import request
from fastapi import FastAPI, requests
from fastapi.responses import JSONResponse

app = FastAPI()
@app.post("/auth/login")
async def login(data: dict):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    if username == "admin" and password == "test123456":
        return {"access-token ": "fake_jwt_token"}
    return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

@app.get("/auth/google")
async def google_auth():
    return {"access-token": "fake_google_jwt_token"}

