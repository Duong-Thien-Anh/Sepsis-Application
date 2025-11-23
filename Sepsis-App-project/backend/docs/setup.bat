@echo off
echo ==========================================
echo   CAI DAT BACKEND - FASTAPI
echo ==========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    pause
    exit /b 1
)

echo [1/3] Tao virtual environment...
if not exist venv (
    python -m venv venv
    echo [OK] Da tao venv
) else (
    echo [OK] venv da ton tai
)

echo.
echo [2/3] Kich hoat venv...
call venv\Scripts\activate.bat

echo.
echo [3/3] Cai dat dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo   CAI DAT HOAN TAT!
echo ==========================================
echo.
echo De chay server, su dung:
echo   run_fastapi.bat
echo.
pause
