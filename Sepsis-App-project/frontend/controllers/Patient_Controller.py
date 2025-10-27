import requests
from tkinter import messagebox
from services.api.api_urls import API_ROUTES
from dotenv import load_dotenv
import time

class PatientController:
    def __init__(self):
        load_dotenv()
        self.api_url = "http://localhost:5000"
        self.timeout = 5
        self._cache = {}  # Cache dữ liệu
        self._cache_duration = 60  # Cache trong 60 giây
    
    # ==================== CRUD OPERATIONS ====================
    
    def get_all_patients(self):
        """Lấy danh sách tất cả bệnh nhân từ API."""
        cache_key = "all_patients"
        
        # Kiểm tra cache
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if time.time() - cached_time < self._cache_duration:
                print("📦 Sử dụng dữ liệu bệnh nhân từ cache")
                return cached_data
        
        try:
            url = API_ROUTES["patient"]["list"]
            print(f"🌐 Đang gọi API: {url}")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            patients = data.get("data", [])
            
            # Lưu vào cache
            self._cache[cache_key] = (time.time(), patients)
            
            print(f"✅ Tải thành công {len(patients)} bệnh nhân")
            return patients
            
        except requests.exceptions.Timeout:
            print("⏰ Timeout khi gọi API")
            return []
        except requests.exceptions.ConnectionError:
            print("❌ Không thể kết nối đến server")
            return []
        except Exception as e:
            print(f"❌ Lỗi khi tải danh sách bệnh nhân: {e}")
            return []
    
    def get_patient_by_id(self, patient_id):
        """Lấy thông tin chi tiết 1 bệnh nhân theo ID."""
        try:
            url = f"{API_ROUTES['patient']['get_by_id']}?id={patient_id}"
            print(f"🌐 Đang gọi API: {url}")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            patient = data.get("data", None)
            
            if patient:
                print(f"✅ Tải thành công bệnh nhân ID: {patient_id}")
            else:
                print(f"⚠️ Không tìm thấy bệnh nhân ID: {patient_id}")
            
            return patient
            
        except requests.exceptions.Timeout:
            print("⏰ Timeout khi gọi API")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Không thể kết nối đến server")
            return None
        except Exception as e:
            print(f"❌ Lỗi khi tải bệnh nhân: {e}")
            return None
    
    def create_patient(self, patient_data):
        """Tạo bệnh nhân mới.
        
        Args:
            patient_data (dict): Dữ liệu bệnh nhân
                - full_name: Họ và tên
                - birth_date: Ngày sinh (YYYY-MM-DD)
                - gender: Giới tính (Nam/Nữ)
                - phone: Số điện thoại
                - email: Email
                
        Returns:
            tuple: (success: bool, message: str, data: dict)
        """
        try:
            url = API_ROUTES["patient"]["create"]
            print(f"🌐 Đang gọi API: {url}")
            print(f"📝 Dữ liệu: {patient_data}")
            
            response = requests.post(url, json=patient_data, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Xóa cache để reload danh sách
            self._clear_cache()
            
            print(f"✅ Tạo bệnh nhân thành công: {patient_data.get('full_name')}")
            return (True, "Tạo bệnh nhân thành công!", data.get("data"))
            
        except requests.exceptions.Timeout:
            print("⏰ Timeout khi gọi API")
            return (False, "Timeout khi kết nối đến server!", None)
        except requests.exceptions.ConnectionError:
            print("❌ Không thể kết nối đến server")
            return (False, "Không thể kết nối đến server!", None)
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.json().get("message", "Lỗi không xác định")
            print(f"❌ Lỗi HTTP: {error_msg}")
            return (False, error_msg, None)
        except Exception as e:
            print(f"❌ Lỗi khi tạo bệnh nhân: {e}")
            return (False, f"Lỗi: {str(e)}", None)
    
    def update_patient(self, patient_id, patient_data):
        """Cập nhật thông tin bệnh nhân.
        
        Args:
            patient_id (str): ID bệnh nhân
            patient_data (dict): Dữ liệu cần cập nhật
            
        Returns:
            tuple: (success: bool, message: str, data: dict)
        """
        try:
            url = f"{API_ROUTES['patient']['update']}?id={patient_id}"
            print(f"🌐 Đang gọi API: {url}")
            print(f"📝 Dữ liệu: {patient_data}")
            
            response = requests.put(url, json=patient_data, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Xóa cache để reload danh sách
            self._clear_cache()
            
            print(f"✅ Cập nhật bệnh nhân thành công: {patient_id}")
            return (True, "Cập nhật thành công!", data.get("data"))
            
        except requests.exceptions.Timeout:
            print("⏰ Timeout khi gọi API")
            return (False, "Timeout khi kết nối đến server!", None)
        except requests.exceptions.ConnectionError:
            print("❌ Không thể kết nối đến server")
            return (False, "Không thể kết nối đến server!", None)
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.json().get("message", "Lỗi không xác định")
            print(f"❌ Lỗi HTTP: {error_msg}")
            return (False, error_msg, None)
        except Exception as e:
            print(f"❌ Lỗi khi cập nhật bệnh nhân: {e}")
            return (False, f"Lỗi: {str(e)}", None)
    
    def delete_patient(self, patient_id):
        """Xóa bệnh nhân.
        
        Args:
            patient_id (str): ID bệnh nhân cần xóa
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            url = f"{API_ROUTES['patient']['delete']}?id={patient_id}"
            print(f"🌐 Đang gọi API: {url}")
            
            response = requests.delete(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Xóa cache để reload danh sách
            self._clear_cache()
            
            print(f"✅ Xóa bệnh nhân thành công: {patient_id}")
            return (True, "Xóa bệnh nhân thành công!")
            
        except requests.exceptions.Timeout:
            print("⏰ Timeout khi gọi API")
            return (False, "Timeout khi kết nối đến server!")
        except requests.exceptions.ConnectionError:
            print("❌ Không thể kết nối đến server")
            return (False, "Không thể kết nối đến server!")
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.json().get("message", "Lỗi không xác định")
            print(f"❌ Lỗi HTTP: {error_msg}")
            return (False, error_msg)
        except Exception as e:
            print(f"❌ Lỗi khi xóa bệnh nhân: {e}")
            return (False, f"Lỗi: {str(e)}")
    
    # ==================== SEARCH & FILTER ====================
    
    def search_patients(self, search_text, patient_list):
        """Tìm kiếm bệnh nhân trong danh sách.
        
        Args:
            search_text (str): Từ khóa tìm kiếm
            patient_list (list): Danh sách bệnh nhân cần tìm
            
        Returns:
            list: Danh sách bệnh nhân phù hợp
        """
        if not search_text or not search_text.strip():
            return patient_list
        
        search_text = search_text.strip().lower()
        matched_patients = []
        
        for patient in patient_list:
            # Tìm trong tất cả các trường
            searchable_text = ' '.join([
                str(patient.get('id', '')),
                str(patient.get('full_name', '')),
                str(patient.get('phone', '')),
                str(patient.get('email', '')),
                str(patient.get('birth_date', '')),
                str(patient.get('gender', ''))
            ]).lower()
            
            if search_text in searchable_text:
                matched_patients.append(patient)
        
        print(f"🔍 Tìm thấy {len(matched_patients)} kết quả cho '{search_text}'")
        return matched_patients
    
    def filter_by_column(self, column_name, patient_list):
        """Lọc hiển thị theo cột (chỉ là logic UI, không filter data).
        
        Args:
            column_name (str): Tên cột cần hiển thị
            patient_list (list): Danh sách bệnh nhân
            
        Returns:
            tuple: (display_columns: tuple, patient_list: list)
        """
        all_columns = ("STT", "ID", "Họ và tên", "Ngày sinh", "Giới tính", "SDT", "Email", "Tác vụ")
        
        if column_name == "Tất cả":
            display_columns = all_columns
        elif column_name == "STT":
            display_columns = ("STT", "Tác vụ")
        elif column_name in all_columns:
            display_columns = ("STT", column_name, "Tác vụ")
        else:
            display_columns = all_columns
        
        print(f"🔍 Lọc hiển thị cột: {display_columns}")
        return (display_columns, patient_list)
    
    # ==================== VALIDATION ====================
    
    def validate_patient_data(self, patient_data):
        """Validate dữ liệu bệnh nhân trước khi gửi API.
        
        Args:
            patient_data (dict): Dữ liệu cần validate
            
        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        # Kiểm tra họ tên
        if not patient_data.get('full_name') or not patient_data['full_name'].strip():
            return (False, "Họ và tên không được để trống!")
        
        # Kiểm tra ngày sinh
        if not patient_data.get('birth_date'):
            return (False, "Ngày sinh không được để trống!")
        
        # Kiểm tra giới tính
        if not patient_data.get('gender') or patient_data['gender'] not in ['Nam', 'Nữ']:
            return (False, "Giới tính phải là Nam hoặc Nữ!")
        
        # Kiểm tra số điện thoại (10 số)
        phone = patient_data.get('phone', '')
        if not phone or not phone.strip():
            return (False, "Số điện thoại không được để trống!")
        if not phone.isdigit() or len(phone) != 10:
            return (False, "Số điện thoại phải có 10 chữ số!")
        
        # Kiểm tra email (basic validation)
        email = patient_data.get('email', '')
        if not email or not email.strip():
            return (False, "Email không được để trống!")
        if '@' not in email or '.' not in email:
            return (False, "Email không hợp lệ!")
        
        return (True, "")
    
    # ==================== HELPER METHODS ====================
    
    def _clear_cache(self):
        """Xóa cache để reload dữ liệu mới."""
        self._cache.clear()
        print("🗑️ Đã xóa cache")
    
    def format_patient_for_display(self, patient, index):
        """Format dữ liệu bệnh nhân để hiển thị trong table.
        
        Args:
            patient (dict): Dữ liệu bệnh nhân từ API
            index (int): Số thứ tự
            
        Returns:
            tuple: Dữ liệu đã format (STT, ID, Họ tên, Ngày sinh, Giới tính, SDT, Email, Tác vụ)
        """
        return (
            str(index),
            patient.get('id', ''),
            patient.get('full_name', ''),
            patient.get('birth_date', ''),
            patient.get('gender', ''),
            patient.get('phone', ''),
            patient.get('email', ''),
            "📋 Xem chi tiết"
        )
