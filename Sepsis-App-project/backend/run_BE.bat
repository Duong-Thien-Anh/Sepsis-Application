@echo off
echo ==============================
echo  Cai dat thu vien Python cho BACKEND
echo ==============================

REM B1: Kiem tra neu chua co virtual env thi tao moi
if not exist venv (
    echo Tao virtual environment...
    python -m venv venv
)

REM B2: Kich hoat virtual environment
call venv\Scripts\activate

REM B3: Cai dat thu vien tu requirements.txt neu co
if exist requirements.txt (
    echo Cai dat thu vien tu requirements.txt...
    pip install -r requirements.txt
) else (
    echo Khong tim thay file requirements.txt, dang cai thu vien mac dinh...
    pip install fastapi uvicorn sqlalchemy pydantic python-dotenv
)

echo ==============================
echo  Hoan tat cai dat thu vien BACKEND
echo ==============================
pause
