@echo off
echo ==========================================
echo   SEPSIS BACKEND - FASTAPI
echo ==========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo Vui long cai dat Python 3.9+ tu https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Kich hoat virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Da kich hoat venv
) else (
    echo [WARNING] Khong tim thay venv. Chay voi Python he thong...
)

echo.
echo [INFO] Khoi dong FastAPI server...
echo [INFO] Server: http://localhost:8000
echo [INFO] Docs: http://localhost:8000/docs
echo.
echo Nhan Ctrl+C de dung server
echo.

REM Chạy server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 3000

pause
