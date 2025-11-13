"""
Test Cases cho Patient API
Kiểm tra tất cả CRUD operations
"""
import pytest
from fastapi import status


class TestPatientAPI:
    """Test suite cho Patient endpoints"""
    
    # ==================== CREATE TESTS ====================
    
    def test_create_patient_success(self, client, sample_patient_data):
        """
        Test tạo patient mới thành công
        """
        response = client.post("/api/v1/patient/", json=sample_patient_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["patient_id"] == sample_patient_data["patient_id"]
        assert data["full_name"] == sample_patient_data["full_name"]
        assert data["gender"] == sample_patient_data["gender"]
    
    
    def test_create_patient_invalid_gender(self, client, sample_patient_data):
        """
        Test tạo patient với gender không hợp lệ
        Chỉ chấp nhận: Nam, Nữ, Khác
        """
        sample_patient_data["gender"] = "Male"  # Invalid
        response = client.post("/api/v1/patient/", json=sample_patient_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_create_patient_invalid_blood_type(self, client, sample_patient_data):
        """
        Test tạo patient với blood_type không hợp lệ
        Chỉ chấp nhận: A+, A-, B+, B-, O+, O-, AB+, AB-
        """
        sample_patient_data["blood_type"] = "C+"  # Invalid
        response = client.post("/api/v1/patient/", json=sample_patient_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_create_patient_duplicate_id(self, client, sample_patient_data):
        """
        Test tạo 2 patients với cùng patient_id
        Phải bị reject vì patient_id là unique
        """
        # Tạo patient đầu tiên
        client.post("/api/v1/patient/", json=sample_patient_data)
        
        # Tạo patient thứ 2 với cùng ID
        response = client.post("/api/v1/patient/", json=sample_patient_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "đã tồn tại" in response.json()["detail"]
    
    
    # ==================== READ TESTS ====================
    
    def test_get_all_patients_empty(self, client):
        """
        Test lấy danh sách patients khi database trống
        """
        response = client.get("/api/v1/patient/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    
    def test_get_all_patients_with_data(self, client, sample_patient_data):
        """
        Test lấy danh sách patients khi có dữ liệu
        """
        # Tạo 3 patients
        for i in range(1, 4):
            patient_data = sample_patient_data.copy()
            patient_data["patient_id"] = f"BN00{i}"
            patient_data["full_name"] = f"Nguyễn Văn {chr(64+i)}"
            client.post("/api/v1/patient/", json=patient_data)
        
        # Lấy danh sách
        response = client.get("/api/v1/patient/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    
    def test_get_patient_by_id_success(self, client, sample_patient_data):
        """
        Test lấy thông tin patient theo ID
        """
        # Tạo patient
        client.post("/api/v1/patient/", json=sample_patient_data)
        
        # Lấy thông tin
        response = client.get(f"/api/v1/patient/{sample_patient_data['patient_id']}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["patient_id"] == sample_patient_data["patient_id"]
        assert data["full_name"] == sample_patient_data["full_name"]
    
    
    def test_get_patient_by_id_not_found(self, client):
        """
        Test lấy patient không tồn tại
        """
        response = client.get("/api/v1/patient/BN999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "không tìm thấy" in response.json()["detail"]
    
    
    def test_pagination(self, client, sample_patient_data):
        """
        Test phân trang với skip và limit
        """
        # Tạo 10 patients
        for i in range(1, 11):
            patient_data = sample_patient_data.copy()
            patient_data["patient_id"] = f"BN{i:03d}"
            patient_data["full_name"] = f"Patient {i}"
            client.post("/api/v1/patient/", json=patient_data)
        
        # Lấy 5 records đầu tiên
        response = client.get("/api/v1/patient/?skip=0&limit=5")
        assert len(response.json()) == 5
        
        # Lấy 5 records tiếp theo
        response = client.get("/api/v1/patient/?skip=5&limit=5")
        assert len(response.json()) == 5
    
    
    # ==================== SEARCH TESTS ====================
    
    def test_search_patients_by_keyword(self, client, sample_patient_data):
        """
        Test tìm kiếm patient theo tên hoặc ID
        """
        # Tạo patients
        patients = [
            {"patient_id": "BN001", "full_name": "Nguyễn Văn A"},
            {"patient_id": "BN002", "full_name": "Trần Thị B"},
            {"patient_id": "BN003", "full_name": "Lê Văn C"}
        ]
        
        for p in patients:
            data = sample_patient_data.copy()
            data.update(p)
            client.post("/api/v1/patient/", json=data)
        
        # Tìm theo tên
        response = client.post("/api/v1/patient/search", json={"keyword": "Nguyễn"})
        assert len(response.json()) == 1
        assert response.json()[0]["patient_id"] == "BN001"
        
        # Tìm theo ID
        response = client.post("/api/v1/patient/search", json={"keyword": "BN002"})
        assert len(response.json()) == 1
        assert response.json()[0]["full_name"] == "Trần Thị B"
    
    
    def test_filter_by_gender(self, client, sample_patient_data):
        """
        Test lọc patients theo giới tính
        """
        # Tạo patients với các giới tính khác nhau
        genders = ["Nam", "Nữ", "Nam", "Khác"]
        for i, gender in enumerate(genders, 1):
            data = sample_patient_data.copy()
            data["patient_id"] = f"BN00{i}"
            data["gender"] = gender
            client.post("/api/v1/patient/", json=data)
        
        # Lọc chỉ lấy Nam
        response = client.get("/api/v1/patient/?gender=Nam")
        assert len(response.json()) == 2
        for patient in response.json():
            assert patient["gender"] == "Nam"
    
    
    # ==================== UPDATE TESTS ====================
    
    def test_update_patient_success(self, client, sample_patient_data):
        """
        Test cập nhật thông tin patient
        """
        # Tạo patient
        client.post("/api/v1/patient/", json=sample_patient_data)
        
        # Cập nhật
        update_data = {
            "full_name": "Nguyễn Văn A Updated",
            "phone_number": "0987654321"
        }
        response = client.put(
            f"/api/v1/patient/{sample_patient_data['patient_id']}",
            json=update_data
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["phone_number"] == update_data["phone_number"]
        # Các field khác không đổi
        assert data["gender"] == sample_patient_data["gender"]
    
    
    def test_update_patient_not_found(self, client):
        """
        Test cập nhật patient không tồn tại
        """
        update_data = {"full_name": "Test"}
        response = client.put("/api/v1/patient/BN999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    # ==================== DELETE TESTS ====================
    
    def test_delete_patient_success(self, client, sample_patient_data):
        """
        Test xóa patient thành công
        """
        # Tạo patient
        client.post("/api/v1/patient/", json=sample_patient_data)
        
        # Xóa
        response = client.delete(f"/api/v1/patient/{sample_patient_data['patient_id']}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "thành công" in response.json()["message"]
        
        # Kiểm tra đã xóa thật
        get_response = client.get(f"/api/v1/patient/{sample_patient_data['patient_id']}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_delete_patient_not_found(self, client):
        """
        Test xóa patient không tồn tại
        """
        response = client.delete("/api/v1/patient/BN999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ==================== EDGE CASES ====================

class TestPatientEdgeCases:
    """Test các trường hợp đặc biệt"""
    
    def test_missing_required_fields(self, client):
        """
        Test tạo patient thiếu trường bắt buộc
        """
        incomplete_data = {
            "patient_id": "BN001"
            # Thiếu full_name, gender, etc.
        }
        response = client.post("/api/v1/patient/", json=incomplete_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_invalid_date_format(self, client, sample_patient_data):
        """
        Test ngày sinh không đúng định dạng
        """
        sample_patient_data["date_of_birth"] = "15/01/1990"  # Sai format
        response = client.post("/api/v1/patient/", json=sample_patient_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_very_long_name(self, client, sample_patient_data):
        """
        Test tên quá dài (boundary test)
        """
        sample_patient_data["full_name"] = "A" * 500  # 500 ký tự
        response = client.post("/api/v1/patient/", json=sample_patient_data)
        
        # Tùy vào validation của bạn, có thể pass hoặc fail
        # Nếu có max_length validator thì sẽ 422
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]
