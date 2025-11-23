# 🔧 Scripts Folder - Testing & Utility Scripts

Folder này chứa các scripts testing và utilities cho backend.

## 📁 Files trong folder:

### ⚡ **test_db_connection.py** (Quick Test)
**Mục đích:** Quick verification của `app/db/session.py`

**Chức năng:**
- ✅ Test Engine creation
- ✅ Test MySQL connection
- ✅ Check MySQL version
- ✅ Verify database name
- ✅ List tables
- ✅ Test SessionLocal factory
- ✅ Test get_db() dependency (FastAPI)
- ✅ Monitor connection pool

**Khi nào dùng:**
- ⚡ Quick smoke test hàng ngày
- 🚀 Trước khi start server
- 🔧 Sau khi sửa session.py
- ✅ Verify FastAPI setup

**Chạy:**
```bash
cd backend
python scripts/test_db_connection.py
```

**Output:**
```
✅ Engine URL: mysql+pymysql://...
✅ Kết nối thành công!
✅ MySQL Version: 8.0.44
✅ Database: sepsis_application
✅ Tìm thấy 9 tables
✅ SessionLocal tạo thành công
✅ get_db() hoạt động
✅ Connection Pool healthy

🎉 TẤT CẢ TESTS ĐỀU PASS!
```

---

### 🧪 **test_mysql_connection.py** (Deep Test)
**Mục đích:** Comprehensive MySQL database testing

**Chức năng:**
- ✅ Test MySQL server connection (raw pymysql)
- ✅ Verify database exists
- ✅ Check all 9 tables created
- ✅ Test SQLAlchemy connection
- ✅ Query sample data
- ✅ Test CRUD operations (INSERT, SELECT, UPDATE, DELETE)

**Khi nào dùng:**
- Setup MySQL lần đầu
- Troubleshoot database issues
- Verify database schema
- Check data integrity
- Learning CRUD operations

**Chạy:**
```bash
cd backend
python scripts/test_mysql_connection.py
```

**Output:**
```
🔍 MySQL Server Connection      ✅ PASS
🔍 Database Exists               ✅ PASS
🔍 Tables Exist                  ✅ PASS
🔍 SQLAlchemy Connection         ✅ PASS
🔍 Query Data                    ✅ PASS
🔍 CRUD Operations               ✅ PASS

🎉 6/6 TESTS PASSED!
```

---

## 🆚 So sánh 2 Test Scripts

### **test_db_connection.py** (Quick - Daily use)
- ⚡ Fast & focused
- 🎯 Test `app/db/session.py` specifically
- 🚀 FastAPI dependency injection
- 📊 Connection pool monitoring
- ✅ Run trước mỗi lần code

### **test_mysql_connection.py** (Comprehensive - Deep dive)
- 🔍 Comprehensive testing
- 🛠️ Troubleshooting tool
- 📚 Educational (CRUD examples)
- 🎨 Fancy output with colors
- ✅ Run when setting up or debugging

---

## 📊 Workflow Recommended

### Setup lần đầu:
```bash
1. python scripts/test_mysql_connection.py   # ← Full check
2. python scripts/test_db_connection.py      # ← Quick verify
3. python run_fastapi.bat                    # ← Start server
```

### Daily development:
```bash
# Quick check trước khi code
python scripts/test_db_connection.py

# Nếu có vấn đề → deep dive
python scripts/test_mysql_connection.py

# Start server
python run_fastapi.bat
```

---

## 🎯 Future Scripts

Folder này có thể chứa thêm:
- `seed_database.py` - Populate sample data
- `backup_database.py` - Backup database
- `migrate_schema.py` - Schema migration
- `generate_test_data.py` - Generate test patients
- `check_performance.py` - Performance testing

---

## 📝 Notes

- Tất cả scripts đọc config từ `.env` file
- Không commit scripts với hardcoded credentials
- Scripts nên có error handling tốt
- Có thể thêm vào `.gitignore` nếu chứa sensitive data
