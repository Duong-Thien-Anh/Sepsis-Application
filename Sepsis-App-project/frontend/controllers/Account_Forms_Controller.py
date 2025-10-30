import re
from tkinter import filedialog
from PIL import Image
import customtkinter as ctk

class AccountFormsController:
    """Controller xử lý logic cho form thêm/sửa tài khoản."""
    
    def __init__(self):
        pass
    
    # ==================== AVATAR UPLOAD ====================
    
    def upload_avatar(self, avatar_label, forms_instance):
        """Upload và hiển thị avatar.
        
        Args:
            avatar_label: CTkLabel để hiển thị avatar
            forms_instance: Instance của AccountForms để lưu avatar_path
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
    
    def validate_account_data(self, account_data, is_edit=False):
        """Validate dữ liệu tài khoản.
        
        Args:
            account_data (dict): Dữ liệu tài khoản cần validate
            is_edit (bool): True nếu đang sửa (không cần validate password)
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Các trường bắt buộc
        required_fields = ["username", "full_name", "email", "role"]
        
        # Nếu là tạo mới, password cũng bắt buộc
        if not is_edit:
            required_fields.append("password")
        
        # Kiểm tra các trường bắt buộc
        for field in required_fields:
            if not account_data.get(field) or str(account_data.get(field)).strip() == "":
                field_names = {
                    "username": "Tên đăng nhập",
                    "password": "Mật khẩu",
                    "full_name": "Họ và tên",
                    "email": "Email",
                    "role": "Vai trò"
                }
                return False, f"Vui lòng nhập {field_names.get(field, field)}!"
        
        # Validate username (chỉ chữ cái, số, gạch dưới, 3-20 ký tự)
        username_pattern = r"^[a-zA-Z0-9_]{3,20}$"
        if not re.match(username_pattern, account_data.get("username", "")):
            return False, "Tên đăng nhập không hợp lệ! (3-20 ký tự, chỉ chữ cái, số, gạch dưới)"
        
        # Validate password (nếu có)
        if account_data.get("password"):
            password = account_data.get("password", "")
            if len(password) < 6:
                return False, "Mật khẩu phải có ít nhất 6 ký tự!"
        
        # Validate email
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, account_data.get("email", "")):
            return False, "Email không hợp lệ!"
        
        # Validate phone nếu có
        if account_data.get("phone") and account_data.get("phone").strip() != "":
            phone_pattern = r"^0\d{9}$"
            if not re.match(phone_pattern, account_data.get("phone", "")):
                return False, "Số điện thoại không hợp lệ! (Phải có 10 chữ số, bắt đầu bằng 0)"
        
        return True, ""
    
    # ==================== DATA PREPARATION ====================
    
    def prepare_api_data(self, account_data):
        """Chuẩn bị dữ liệu để gửi lên API.
        
        Args:
            account_data (dict): Dữ liệu tài khoản đã validate
            
        Returns:
            dict: Dữ liệu đã chuẩn bị cho API
        """
        # Loại bỏ các trường trống hoặc None
        api_data = {}
        for key, value in account_data.items():
            if value is not None and (isinstance(value, str) and value.strip() != "" or not isinstance(value, str)):
                api_data[key] = value.strip() if isinstance(value, str) else value
        
        return api_data
