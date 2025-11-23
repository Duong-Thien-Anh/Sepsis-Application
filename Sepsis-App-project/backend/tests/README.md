# 🧪 Testing Guide - Hướng Dẫn Test

## 📋 Tổng Quan

Folder này chứa **automated tests** để kiểm tra API hoạt động đúng không.

## 📁 Cấu Trúc

```
tests/
├── conftest.py              # ⚙️ Setup & fixtures dùng chung
├── test_patient_api.py      # 🧪 Test Patient CRUD operations
├── test_employee_api.py     # (TODO) Test Employee endpoints
├── test_predict_api.py      # (TODO) Test AI prediction
└── README.md                # 📖 File này
```

## 🚀 Cách Chạy Tests

### 1️⃣ Cài Đặt Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2️⃣ Chạy Tất Cả Tests

```bash
pytest
```

### 3️⃣ Chạy Test Cụ Thể

```bash
# Chỉ test Patient API
pytest tests/test_patient_api.py

# Chỉ test 1 function cụ thể
pytest tests/test_patient_api.py::TestPatientAPI::test_create_patient_success

# Test theo keyword
pytest -k "create"  # Chạy tất cả tests có "create" trong tên
```

### 4️⃣ Xem Kết Quả Chi Tiết

```bash
# Verbose mode - hiển thị chi tiết
pytest -v

# Hiển thị print statements
pytest -s

# Dừng lại khi gặp lỗi đầu tiên
pytest -x

# Kết hợp
pytest -vsx
```

### 5️⃣ Kiểm Tra Coverage (Độ phủ code)

```bash
# Cài coverage
pip install pytest-cov

# Chạy với coverage report
pytest --cov=app --cov-report=html

# Mở file htmlcov/index.html để xem báo cáo
```

## 📝 Cấu Trúc 1 Test Case

```python
def test_feature_name(self, client, sample_patient_data):
    """
    Mô tả: Test làm gì
    """
    # 1. ARRANGE - Chuẩn bị dữ liệu
    patient_data = sample_patient_data.copy()
    
    # 2. ACT - Thực hiện action
    response = client.post("/api/v1/patient/", json=patient_data)
    
    # 3. ASSERT - Kiểm tra kết quả
    assert response.status_code == 200
    assert response.json()["patient_id"] == patient_data["patient_id"]
```

## 🎯 Các Loại Tests Đã Viết

### ✅ Test CRUD Operations
- **CREATE**: Tạo patient mới
  - ✅ Tạo thành công
  - ✅ Validate gender (Nam/Nữ/Khác)
  - ✅ Validate blood_type (A+, O-, etc.)
  - ✅ Reject duplicate ID

- **READ**: Đọc dữ liệu
  - ✅ Lấy tất cả patients
  - ✅ Lấy patient theo ID
  - ✅ Pagination (skip/limit)
  - ✅ Filter theo gender
  - ✅ Search theo keyword

- **UPDATE**: Cập nhật
  - ✅ Update thành công
  - ✅ Chỉ update fields được gửi
  - ✅ 404 nếu patient không tồn tại

- **DELETE**: Xóa
  - ✅ Xóa thành công
  - ✅ 404 nếu patient không tồn tại

### ✅ Edge Cases (Trường hợp đặc biệt)
- ✅ Thiếu trường bắt buộc
- ✅ Định dạng ngày sai
- ✅ Tên quá dài

## 🔍 Hiểu conftest.py

`conftest.py` chứa các **fixtures** - code setup dùng chung:

### 1. `db_session` Fixture
```python
@pytest.fixture
def db_session():
    # Tạo SQLite in-memory database cho test
    # Không ảnh hưởng MySQL thật!
```

**Lợi ích:**
- ✅ Mỗi test có database sạch
- ✅ Không làm bẩn database production
- ✅ Test chạy nhanh hơn

### 2. `client` Fixture
```python
@pytest.fixture
def client(db_session):
    # TestClient để gọi API như HTTP request
```

**Sử dụng:**
```python
def test_example(client):
    response = client.get("/api/v1/patient/")
    assert response.status_code == 200
```

### 3. `sample_patient_data` Fixture
```python
@pytest.fixture
def sample_patient_data():
    # Dữ liệu patient mẫu
```

**Sử dụng:**
```python
def test_create(client, sample_patient_data):
    response = client.post("/api/v1/patient/", json=sample_patient_data)
```

## 📊 Ví Dụ Output

```
tests/test_patient_api.py::TestPatientAPI::test_create_patient_success PASSED     [ 10%]
tests/test_patient_api.py::TestPatientAPI::test_create_patient_invalid_gender PASSED [ 20%]
tests/test_patient_api.py::TestPatientAPI::test_get_all_patients_empty PASSED     [ 30%]
...
========================== 20 passed in 2.45s ==========================
```

## 🎓 Best Practices

### ✅ DO (Nên làm)
- ✅ Test cả happy path VÀ error cases
- ✅ Test tên nên mô tả rõ ràng: `test_create_patient_with_invalid_gender`
- ✅ Mỗi test chỉ test 1 điều
- ✅ Dùng fixtures để tránh duplicate code
- ✅ Assert cả status code VÀ response data

### ❌ DON'T (Không nên)
- ❌ Dùng database thật trong test
- ❌ Tests phụ thuộc vào nhau (test A phải chạy trước test B)
- ❌ Hardcode data, dùng fixtures thay vào
- ❌ Test quá dài (>50 dòng), nên tách nhỏ

## 🔧 Troubleshooting

### ❗ Lỗi: "No module named pytest"
```bash
pip install pytest
```

### ❗ Lỗi: "No tests ran"
- Kiểm tra test file phải bắt đầu bằng `test_`
- Kiểm tra test function phải bắt đầu bằng `test_`

### ❗ Lỗi: Database connection
- Kiểm tra `.env` file
- Test dùng SQLite in-memory, không cần MySQL running

## 📚 Tài Liệu Tham Khảo

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html)

## 🚀 Next Steps

1. **Chạy tests hiện tại:**
   ```bash
   pytest -v
   ```

2. **Viết tests cho Employee API:**
   - Copy `test_patient_api.py`
   - Sửa endpoints và data
   
3. **Viết tests cho Predict API:**
   - Test AI prediction logic
   - Mock model nếu cần

4. **Setup CI/CD:**
   - GitHub Actions tự động chạy tests khi push code
