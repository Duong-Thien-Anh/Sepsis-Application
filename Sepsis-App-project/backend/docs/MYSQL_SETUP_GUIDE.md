# 🔧 HƯỚNG DẪN KẾT NỐI MYSQL CHO BACKEND

## 📋 YÊU CẦU

- ✅ Python 3.9+
- ✅ MySQL Server 8.0+ (hoặc 5.7+)
- ✅ MySQL Workbench (khuyến nghị để quản lý database)

---

## 🚀 BƯỚC 1: CÀI ĐẶT MYSQL

### Tải MySQL:
👉 https://dev.mysql.com/downloads/installer/

### Cài đặt:
1. Chọn "MySQL Server"
2. Đặt **root password** (nhớ password này!)
3. Port mặc định: **3306**

### Kiểm tra MySQL đã chạy:
```bash
# Mở MySQL Command Line hoặc MySQL Workbench
mysql -u root -p
```

---

## 🗄️ BƯỚC 2: TẠO DATABASE

### Cách 1: Dùng MySQL Workbench (GIÁ KHUYẾN NGHỊ)

1. **Mở MySQL Workbench**
2. **Kết nối** với MySQL Server (localhost:3306)
3. **Chạy script** `database_mysql.sql`:
   - Menu: File → Open SQL Script
   - Chọn file: `backend/database_mysql.sql`
   - Click ⚡ Execute (hoặc Ctrl+Shift+Enter)

### Cách 2: Dùng Command Line

```bash
# Mở Command Prompt/PowerShell
cd "C:\Users\ngogi\OneDrive\Máy tính\Sepsis-Application\Sepsis-App-project\backend"

# Chạy script
mysql -u root -p < database_mysql.sql
# Nhập password khi được hỏi
```

### ✅ Kiểm tra database đã tạo:

```sql
-- Trong MySQL Workbench hoặc mysql command line
SHOW DATABASES;
USE sepsis_management;
SHOW TABLES;
```

Bạn sẽ thấy:
```
+----------------------------+
| Tables_in_sepsis_management|
+----------------------------+
| Account                    |
| Employee                   |
| Patient                    |
| MedicalHistoryRecord       |
| Diagnosis                  |
| TestResult                 |
| AIResult                   |
| RecallAppointment          |
| ActivityLog                |
+----------------------------+
```

---

## ⚙️ BƯỚC 3: CẤU HÌNH KẾT NỐI

### Mở file `.env`:
```
backend/.env
```

### Chỉnh sửa thông tin MySQL của bạn:

```env
# ========================================
# MYSQL DATABASE CONFIGURATION
# ========================================
MYSQL_USER=root                    # ← Username MySQL của bạn
MYSQL_PASSWORD=your_password       # ← Password MySQL của bạn
MYSQL_HOST=localhost               # ← localhost hoặc IP server
MYSQL_PORT=3306                    # ← Port MySQL (mặc định 3306)
MYSQL_DATABASE=sepsis_management   # ← Tên database vừa tạo
```

### 📝 **VÍ DỤ CẤU HÌNH:**

```env
# Nếu bạn dùng root với password là "123456"
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=sepsis_management

# Nếu không có password (KHÔNG KHUYẾN NGHỊ cho production)
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=sepsis_management
```

---

## 🔧 BƯỚC 4: CÀI ĐẶT DEPENDENCIES

```powershell
# Từ thư mục backend/
cd "C:\Users\ngogi\OneDrive\Máy tính\Sepsis-Application\Sepsis-App-project\backend"

# Cài đặt
pip install -r requirements.txt
```

Hoặc dùng script:
```bash
setup.bat
```

---

## ▶️ BƯỚC 5: CHẠY SERVER

```bash
# Cách 1: Dùng script
run_fastapi.bat

# Cách 2: Chạy thủ công
python -m uvicorn app.main:app --reload --port 3000
```

### ✅ Kiểm tra kết nối thành công:

Khi server chạy, bạn sẽ thấy:
```
🔌 Connecting to MySQL: localhost:3306/sepsis_management
INFO:     Uvicorn running on http://127.0.0.1:3000 (Press CTRL+C to quit)
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**KHÔNG CÓ LỖI** = Kết nối thành công! ✅

---

## 🧪 BƯỚC 6: TEST API

### 1. Mở Swagger UI:
👉 http://localhost:3000/docs

### 2. Test endpoint "GET /api/v1/patient/":
- Click endpoint
- Click "Try it out"
- Click "Execute"

### 3. Kết quả mong đợi:
```json
{
  "patients": [
    {
      "patient_id": "BN001",
      "full_name": "Tran Thi B",
      "gender": "Nữ",
      ...
    },
    {
      "patient_id": "BN002",
      "full_name": "Le Van C",
      "gender": "Nam",
      ...
    }
  ],
  "total": 2,
  "pages": 1,
  "current_page": 1
}
```

---

## 🐛 TROUBLESHOOTING

### ❌ Lỗi: "Access denied for user"
**Nguyên nhân:** Sai username hoặc password

**Giải pháp:**
1. Kiểm tra file `.env`
2. Đảm bảo username/password đúng
3. Test kết nối bằng MySQL Workbench trước

### ❌ Lỗi: "Can't connect to MySQL server"
**Nguyên nhân:** MySQL chưa chạy

**Giải pháp:**
1. Mở Services (Windows+R → `services.msc`)
2. Tìm "MySQL80" (hoặc phiên bản của bạn)
3. Click "Start"

### ❌ Lỗi: "Unknown database 'sepsis_management'"
**Nguyên nhân:** Chưa chạy script tạo database

**Giải pháp:**
```bash
mysql -u root -p < database_mysql.sql
```

### ❌ Lỗi: "No module named 'pymysql'"
**Nguyên nhân:** Chưa cài PyMySQL

**Giải pháp:**
```bash
pip install pymysql cryptography
```

---

## 📊 CẤU TRÚC DATABASE

```
sepsis_management (Database)
├── Account              (Tài khoản)
├── Employee             (Nhân viên)
├── Patient              (Bệnh nhân) ← Đã có data mẫu
├── MedicalHistoryRecord (Hồ sơ bệnh án)
├── Diagnosis            (Chẩn đoán)
├── TestResult           (Kết quả xét nghiệm)
├── AIResult             (Kết quả AI)
├── RecallAppointment    (Lịch hẹn)
└── ActivityLog          (Log hoạt động)
```

---

## 🎯 KIỂM TRA KẾT NỐI TRỰC TIẾP

### Script Python test connection:

```python
# test_mysql_connection.py
import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='your_password',  # ← Thay password của bạn
        database='sepsis_management',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as total FROM Patient")
        result = cursor.fetchone()
        print(f"✅ Kết nối thành công!")
        print(f"📊 Tổng số bệnh nhân: {result['total']}")
    
    connection.close()
    
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
```

Chạy:
```bash
python test_mysql_connection.py
```

---

## 🎉 HOÀN TẤT!

Bây giờ bạn đã có:
- ✅ MySQL database hoạt động
- ✅ Backend FastAPI kết nối MySQL
- ✅ API endpoints sẵn sàng
- ✅ Dữ liệu mẫu để test

**Tiếp theo:**
- Test các API endpoints tại: http://localhost:3000/docs
- Kết nối Frontend Desktop App với API
- Thêm dữ liệu thật vào database

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra MySQL đang chạy
2. Kiểm tra file `.env` đúng cấu hình
3. Xem log lỗi khi chạy server
4. Test kết nối với script Python ở trên
