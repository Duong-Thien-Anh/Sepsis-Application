"""
Controller xử lý logic cho các form thêm/sửa bệnh nhân.
"""
from tkinter import filedialog
from PIL import Image
import os

class PatientFormsController:
    """Controller cho các form thêm/sửa bệnh nhân."""
    
    def __init__(self):
        """Khởi tạo controller."""
        pass
    
    def upload_avatar(self, avatar_label, on_success_callback, on_error_callback):
        """
        Mở dialog chọn ảnh và xử lý upload.
        
        Args:
            avatar_label: CTkLabel để hiển thị ảnh
            on_success_callback: Callback(image, file_path) khi thành công
            on_error_callback: Callback(error_msg) khi có lỗi
        """
        try:
            # Mở hộp thoại chọn file
            file_path = filedialog.askopenfilename(
                title="Chọn ảnh đại diện",
                filetypes=[
                    ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("All files", "*.*")
                ]
            )
            
            if not file_path:
                return  # User cancelled
            
            # Kiểm tra file tồn tại
            if not os.path.exists(file_path):
                on_error_callback("File không tồn tại!")
                return
            
            # Mở và resize ảnh
            image = Image.open(file_path)
            
            # Resize ảnh để fit vào khung 200x283
            image.thumbnail((200, 283), Image.Resampling.LANCZOS)
            
            # Callback thành công
            on_success_callback(image, file_path)
            
        except Exception as e:
            on_error_callback(f"Lỗi khi tải ảnh: {str(e)}")
    
    def validate_patient_data(self, fields_dict):
        """
        Validate dữ liệu bệnh nhân từ form.
        
        Args:
            fields_dict: Dictionary chứa các widget input
            
        Returns:
            (is_valid, error_message, patient_data)
        """
        try:
            # Lấy dữ liệu từ các field
            patient_data = {}
            
            # Các field bắt buộc
            required_fields = {
                'họ_và_tên': 'Họ và tên',
                'ngày_sinh': 'Ngày sinh',
                'giới_tính': 'Giới tính',
                'số_điện_thoại': 'Số điện thoại'
            }
            
            # Kiểm tra các field bắt buộc
            for field_key, field_name in required_fields.items():
                if field_key not in fields_dict:
                    continue
                    
                widget = fields_dict[field_key]
                
                # Lấy giá trị tùy theo loại widget
                if hasattr(widget, 'get'):
                    if hasattr(widget, 'get') and callable(widget.get):
                        value = widget.get()
                        if isinstance(value, str):
                            value = value.strip()
                    else:
                        value = ""
                else:
                    value = ""
                
                if not value:
                    return False, f"{field_name} không được để trống!", None
                
                patient_data[field_key] = value
            
            # Lấy các field không bắt buộc
            optional_fields = [
                'email', 'địa_chỉ', 'chức_vụ', 'ngày_bắt_đầu_làm_việc',
                'cân_nặng_(kg)', 'tiểu_sử_bệnh_lý', 'tên_người_thân',
                'số_điện_thoại_người_thân', 'quan_hệ_người_thân', 'ghi_chú'
            ]
            
            for field_key in optional_fields:
                if field_key not in fields_dict:
                    continue
                    
                widget = fields_dict[field_key]
                
                # Lấy giá trị
                if hasattr(widget, 'get'):
                    if field_key in ['tiểu_sử_bệnh_lý', 'ghi_chú']:
                        # CTkTextbox
                        value = widget.get("1.0", "end-1c").strip()
                    else:
                        # CTkEntry hoặc CTkOptionMenu
                        value = widget.get()
                        if isinstance(value, str):
                            value = value.strip()
                else:
                    value = ""
                
                patient_data[field_key] = value
            
            return True, "", patient_data
            
        except Exception as e:
            return False, f"Lỗi khi validate: {str(e)}", None
    
    def prepare_api_data(self, patient_data):
        """
        Chuẩn bị dữ liệu để gửi API.
        
        Args:
            patient_data: Dictionary chứa dữ liệu bệnh nhân
            
        Returns:
            Dictionary với format phù hợp cho API
        """
        # Mapping từ key UI sang key API
        api_data = {
            'full_name': patient_data.get('họ_và_tên', ''),
            'birth_date': patient_data.get('ngày_sinh', ''),
            'gender': patient_data.get('giới_tính', ''),
            'phone': patient_data.get('số_điện_thoại', ''),
            'email': patient_data.get('email', ''),
            'address': patient_data.get('địa_chỉ', ''),
            'position': patient_data.get('chức_vụ', ''),
            'start_date': patient_data.get('ngày_bắt_đầu_làm_việc', ''),
            'weight': patient_data.get('cân_nặng_(kg)', ''),
            'medical_history': patient_data.get('tiểu_sử_bệnh_lý', ''),
            'emergency_contact_name': patient_data.get('tên_người_thân', ''),
            'emergency_contact_phone': patient_data.get('số_điện_thoại_người_thân', ''),
            'emergency_contact_relation': patient_data.get('quan_hệ_người_thân', ''),
            'notes': patient_data.get('ghi_chú', '')
        }
        
        return api_data
