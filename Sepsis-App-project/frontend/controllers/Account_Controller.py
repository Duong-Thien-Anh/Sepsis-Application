import re

class AccountController:
    """Controller xử lý logic nghiệp vụ cho quản lý tài khoản."""
    
    def __init__(self):
        pass
    
    # ==================== VALIDATION ====================
    
    def validate_account_data(self, account_data, is_edit=False):
        """Validate dữ liệu tài khoản.
        
        Args:
            account_data (dict): Dữ liệu tài khoản cần validate
            is_edit (bool): True nếu đang sửa tài khoản (không cần validate password)
            
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
        if account_data.get("phone"):
            phone_pattern = r"^0\d{9}$"
            if not re.match(phone_pattern, account_data.get("phone", "")):
                return False, "Số điện thoại không hợp lệ! (Phải có 10 chữ số, bắt đầu bằng 0)"
        
        return True, ""
    
    # ==================== FILTER & SEARCH ====================
    
    def filter_by_column(self, accounts, column, search_text):
        """Lọc danh sách tài khoản theo cột.
        
        Args:
            accounts (list): Danh sách tài khoản
            column (str): Tên cột cần lọc
            search_text (str): Nội dung tìm kiếm
            
        Returns:
            list: Danh sách tài khoản đã lọc
        """
        if not search_text:
            return accounts
        
        search_text = search_text.lower()
        filtered = []
        
        column_map = {
            "Tất cả": None,
            "ID": "id",
            "Tên đăng nhập": "username",
            "Họ và tên": "full_name",
            "Email": "email",
            "Vai trò": "role",
            "Trạng thái": "status"
        }
        
        field = column_map.get(column)
        
        for account in accounts:
            if field is None:  # Tìm trong tất cả
                search_in = f"{account.get('id', '')} {account.get('username', '')} {account.get('full_name', '')} {account.get('email', '')} {account.get('role', '')} {account.get('status', '')}".lower()
            else:
                search_in = str(account.get(field, "")).lower()
            
            if search_text in search_in:
                filtered.append(account)
        
        return filtered
    
    def search_accounts(self, search_text, filter_column="Tất cả"):
        """Tìm kiếm tài khoản.
        
        Args:
            search_text (str): Nội dung tìm kiếm
            filter_column (str): Cột cần lọc
            
        Returns:
            list: Danh sách tài khoản tìm được
        """
        # TODO: Gọi API để tìm kiếm
        # accounts = api_client.search_accounts(search_text, filter_column)
        # return accounts
        
        # Giả lập dữ liệu
        return []
    
    # ==================== CRUD OPERATIONS ====================
    
    def get_all_accounts(self):
        """Lấy danh sách tất cả tài khoản.
        
        Returns:
            list: Danh sách tài khoản
        """
        # TODO: Gọi API để lấy danh sách
        # accounts = api_client.get_all_accounts()
        # return accounts
        
        # Giả lập dữ liệu
        return []
    
    def get_account_by_id(self, account_id):
        """Lấy thông tin tài khoản theo ID.
        
        Args:
            account_id (str): ID tài khoản
            
        Returns:
            dict: Thông tin tài khoản
        """
        # TODO: Gọi API để lấy thông tin
        # account = api_client.get_account_by_id(account_id)
        # return account
        
        # Giả lập dữ liệu
        return None
    
    def create_account(self, account_data):
        """Tạo tài khoản mới.
        
        Args:
            account_data (dict): Dữ liệu tài khoản
            
        Returns:
            bool: True nếu tạo thành công
        """
        # TODO: Gọi API để tạo tài khoản
        # success = api_client.create_account(account_data)
        # return success
        
        # Giả lập
        return True
    
    def update_account(self, account_id, account_data):
        """Cập nhật thông tin tài khoản.
        
        Args:
            account_id (str): ID tài khoản
            account_data (dict): Dữ liệu cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công
        """
        # TODO: Gọi API để cập nhật
        # success = api_client.update_account(account_id, account_data)
        # return success
        
        # Giả lập
        return True
    
    def delete_account(self, account_id):
        """Xóa tài khoản.
        
        Args:
            account_id (str): ID tài khoản
            
        Returns:
            bool: True nếu xóa thành công
        """
        # TODO: Gọi API để xóa
        # success = api_client.delete_account(account_id)
        # return success
        
        # Giả lập
        return True
    
    def change_password(self, account_id, old_password, new_password):
        """Đổi mật khẩu tài khoản.
        
        Args:
            account_id (str): ID tài khoản
            old_password (str): Mật khẩu cũ
            new_password (str): Mật khẩu mới
            
        Returns:
            tuple: (success, message)
        """
        # Validate mật khẩu mới
        if len(new_password) < 6:
            return False, "Mật khẩu mới phải có ít nhất 6 ký tự!"
        
        # TODO: Gọi API để đổi mật khẩu
        # success = api_client.change_password(account_id, old_password, new_password)
        # return success, "Đổi mật khẩu thành công!" if success else "Đổi mật khẩu thất bại!"
        
        # Giả lập
        return True, "Đổi mật khẩu thành công!"
