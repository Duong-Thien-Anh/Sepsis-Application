import re
from tkinter import filedialog
from PIL import Image
import customtkinter as ctk

class EmployeeFormsController:
    """Controller xử lý logic cho form thêm/sửa nhân viên."""
    
    def __init__(self):
        pass
    
    # ==================== AVATAR UPLOAD ====================
    
    def upload_avatar(self, avatar_label, forms_instance):
        """Upload và hiển thị avatar.
        
        Args:
            avatar_label: CTkLabel để hiển thị avatar
            forms_instance: Instance của EmployeeForms để lưu avatar_path
        """
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh đại diện",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Load và resize ảnh
                image = Image.open(file_path)
                image.thumbnail((200, 283), Image.Resampling.LANCZOS)
                
                # Tạo CTkImage và hiển thị
                ctk_image = ctk.CTkImage(light_image=image, size=image.size)
                avatar_label.configure(image=ctk_image, text="")
                avatar_label.image = ctk_image  # Giữ reference
                
                # Lưu đường dẫn ảnh
                forms_instance.avatar_path = file_path
                
            except Exception as e:
                avatar_label.configure(text=f"Lỗi: {str(e)}")
    
    # ==================== VALIDATION ====================
    
    def validate_employee_data(self, employee_data):
        """Validate dữ liệu nhân viên.
        
        Args:
            employee_data (dict): Dữ liệu nhân viên cần validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Các trường bắt buộc
        required_fields = [
            "full_name", "birth_date", "gender", "citizen_id",
            "phone", "email", "address", "position", 
            "department", "start_date", "status"
        ]
        
        # Kiểm tra các trường bắt buộc
        for field in required_fields:
            if not employee_data.get(field) or employee_data.get(field).strip() == "":
                field_names = {
                    "full_name": "Họ và tên",
                    "birth_date": "Ngày sinh",
                    "gender": "Giới tính",
                    "citizen_id": "CCCD/CMND",
                    "phone": "SDT",
                    "email": "Email",
                    "address": "Địa chỉ",
                    "position": "Chức vụ",
                    "department": "Phòng ban",
                    "start_date": "Ngày bắt đầu làm việc",
                    "status": "Trạng thái"
                }
                return False, f"Vui lòng nhập {field_names.get(field, field)}!"
        
        # Validate số điện thoại (10 chữ số, bắt đầu bằng 0)
        phone_pattern = r"^0\d{9}$"
        if not re.match(phone_pattern, employee_data.get("phone", "")):
            return False, "Số điện thoại không hợp lệ! (Phải có 10 chữ số, bắt đầu bằng 0)"
        
        # Validate email
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, employee_data.get("email", "")):
            return False, "Email không hợp lệ!"
        
        # Validate ngày sinh (DD/MM/YYYY)
        date_pattern = r"^\d{2}/\d{2}/\d{4}$"
        if not re.match(date_pattern, employee_data.get("birth_date", "")):
            return False, "Ngày sinh không hợp lệ! (Định dạng: DD/MM/YYYY)"
        
        # Validate ngày bắt đầu làm việc (DD/MM/YYYY)
        if not re.match(date_pattern, employee_data.get("start_date", "")):
            return False, "Ngày bắt đầu làm việc không hợp lệ! (Định dạng: DD/MM/YYYY)"
        
        # Validate CCCD/CMND (9 hoặc 12 chữ số)
        citizen_id = employee_data.get("citizen_id", "")
        if not (citizen_id.isdigit() and (len(citizen_id) == 9 or len(citizen_id) == 12)):
            return False, "CCCD/CMND không hợp lệ! (Phải có 9 hoặc 12 chữ số)"
        
        return True, ""
    
    # ==================== DATA PREPARATION ====================
    
    def prepare_api_data(self, employee_data):
        """Chuẩn bị dữ liệu để gửi lên API.
        
        Args:
            employee_data (dict): Dữ liệu nhân viên đã validate
            
        Returns:
            dict: Dữ liệu đã chuẩn bị cho API
        """
        # Loại bỏ các trường trống hoặc None
        api_data = {}
        for key, value in employee_data.items():
            if value is not None and (isinstance(value, str) and value.strip() != "" or not isinstance(value, str)):
                api_data[key] = value.strip() if isinstance(value, str) else value
        
        return api_data
