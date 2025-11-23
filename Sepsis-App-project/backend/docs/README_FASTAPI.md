# 🚀 HƯỚNG DẪN CHẠY BACKEND FASTAPI

## 📋 Yêu cầu hệ thống

- Python 3.9+
- SQL Server
- ODBC Driver 17 for SQL Server

## 🔧 Cài đặt

### 1. Tạo virtual environment (khuyến nghị)

```powershell
# Tạo venv
python -m venv venv

# Kích hoạt venv
.\venv\Scripts\Activate.ps1
```

### 2. Cài đặt dependencies

```powershell
pip install -r requirements.txt
```

## ▶️ Chạy ứng dụng

### Cách 1: Chạy trực tiếp với Python

```powershell
# Từ thư mục backend/
python -m app.main
```

### Cách 2: Chạy với uvicorn (khuyến nghị)

```powershell
# Từ thư mục backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Tham số:**
- `--reload`: Auto reload khi code thay đổi
- `--host 0.0.0.0`: Cho phép truy cập từ máy khác
- `--port 8000`: Port của server

## 📚 API Documentation

Sau khi chạy server, truy cập:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Test API

### Sử dụng Swagger UI

1. Mở trình duyệt: http://localhost:8000/docs
2. Chọn endpoint muốn test
3. Click "Try it out"
4. Nhập dữ liệu và Execute

### Sử dụng curl

```powershell
# GET all patients
curl http://localhost:8000/api/v1/patient/

# GET patient by ID
curl http://localhost:8000/api/v1/patient/BN001

# POST create patient
curl -X POST http://localhost:8000/api/v1/patient/ `
  -H "Content-Type: application/json" `
  -d '{
    "patient_id": "BN001",
    "full_name": "Nguyen Van A",
    "gender": "Nam",
    "phone": "0123456789"
  }'

# PUT update patient
curl -X PUT http://localhost:8000/api/v1/patient/BN001 `
  -H "Content-Type: application/json" `
  -d '{
    "phone": "0987654321"
  }'

# DELETE patient
curl -X DELETE http://localhost:8000/api/v1/patient/BN001
```

## 📊 API Endpoints (Patient)

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/patient/` | Lấy danh sách bệnh nhân (có pagination) |
| GET | `/api/v1/patient/{id}` | Lấy thông tin 1 bệnh nhân |
| POST | `/api/v1/patient/search` | Tìm kiếm bệnh nhân theo mã |
| POST | `/api/v1/patient/` | Tạo bệnh nhân mới |
| PUT | `/api/v1/patient/{id}` | Cập nhật bệnh nhân |
| DELETE | `/api/v1/patient/{id}` | Xóa bệnh nhân |

### Query Parameters (GET list)

- `page`: Số trang (default: 1)
- `per_page`: Số record/trang (default: 10, max: 100)
- `search`: Tìm kiếm theo tên
- `gender`: Lọc theo giới tính

**Ví dụ:**
```
GET /api/v1/patient/?page=1&per_page=20&search=nguyen&gender=Nam
```

## 🗂️ Cấu trúc thư mục mới

```
backend/
├── app/
│   ├── main.py              # Entry point
│   ├── api/
│   │   └── v1/
│   │       └── patient.py   # Patient routes
│   ├── crud/
│   │   └── patient.py       # Database operations
│   ├── models/
│   │   └── models.py        # ORM models
│   ├── schemas/
│   │   └── patient.py       # Pydantic schemas
│   └── db/
│       └── session.py       # DB connection
└── requirements.txt
```

## 🔄 So sánh API cũ vs mới

### Flask (cũ) → FastAPI (mới)

| Flask | FastAPI |
|-------|---------|
| `POST /api/patient/search` | `POST /api/v1/patient/search` |
| `POST /api/patient/save` | `POST /api/v1/patient/` (create) |
| | `PUT /api/v1/patient/{id}` (update) |
| `GET /api/patient/list` | `GET /api/v1/patient/` |
| `GET /api/patient/<id>` | `GET /api/v1/patient/{id}` |
| `DELETE /api/patient/<id>` | `DELETE /api/v1/patient/{id}` |

## ⚙️ Cấu hình Database

File: `app/db/session.py`

```python
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"  # Thay đổi nếu cần
    "DATABASE=APP_SepsisManagement;"
    "Trusted_Connection=yes;"
)
```

## 🐛 Troubleshooting

### Lỗi: ModuleNotFoundError

```powershell
# Đảm bảo chạy từ thư mục backend/
cd backend
python -m app.main
```

### Lỗi: Database connection failed

- Kiểm tra SQL Server đang chạy
- Kiểm tra tên database: `APP_SepsisManagement`
- Kiểm tra ODBC Driver 17 đã cài đặt

### Lỗi: Port 8000 đã được sử dụng

```powershell
# Chạy trên port khác
uvicorn app.main:app --port 8001
```

## 📝 TODO

- [ ] Migrate Employee routes
- [ ] Migrate Predict routes
- [ ] Migrate Statistics routes
- [ ] Migrate Authentication routes
- [ ] Thêm unit tests
- [ ] Thêm logging
- [ ] Thêm rate limiting
- [ ] Thêm authentication middleware

## 🎉 Hoàn thành!

Server FastAPI đang chạy tại: http://localhost:8000

Xem docs tại: http://localhost:8000/docs
