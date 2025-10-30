"""
Controller xử lý logic cho quản lý nhân viên.
"""
import re
from datetime import datetime

class EmployeeController:
    """Controller cho quản lý nhân viên."""
    
    def __init__(self):
        """Khởi tạo controller."""
        self.employees = []  # Cache danh sách nhân viên
    
    def validate_employee_data(self, employee_data):
        """
        Validate dữ liệu nhân viên.
        
        Args:
            employee_data (dict): Dictionary chứa thông tin nhân viên
            
        Returns:
            (is_valid, error_message): Tuple gồm boolean và message
        """
        # Kiểm tra họ tên
        if not employee_data.get('full_name'):
            return False, "Họ và tên không được để trống!"
        
        if len(employee_data['full_name']) < 2:
            return False, "Họ và tên phải có ít nhất 2 ký tự!"
        
        # Kiểm tra ngày sinh
        if not employee_data.get('birth_date'):
            return False, "Ngày sinh không được để trống!"
        
        # Validate format ngày sinh (DD/MM/YYYY)
        birth_date = employee_data['birth_date']
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', birth_date):
            return False, "Ngày sinh phải có định dạng DD/MM/YYYY!"
        
        # Kiểm tra số điện thoại
        if not employee_data.get('phone'):
            return False, "Số điện thoại không được để trống!"
        
        phone = employee_data['phone']
        if not re.match(r'^0\d{9}$', phone):
            return False, "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0!"
        
        # Kiểm tra email (nếu có)
        if employee_data.get('email'):
            email = employee_data['email']
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                return False, "Email không đúng định dạng!"
        
        return True, ""
    
    def filter_by_column(self, selected_column, all_columns):
        """
        Lọc các cột hiển thị.
        
        Args:
            selected_column (str): Tên cột được chọn
            all_columns (list): Danh sách tất cả các cột
            
        Returns:
            (display_columns, hidden_columns): Tuple gồm 2 list
        """
        if selected_column == "Tất cả":
            return all_columns, []
        
        # Mapping tên cột hiển thị -> column ID
        column_map = {
            "STT": "STT",
            "ID": "ID",
            "Họ và tên": "Họ và tên",
            "Ngày sinh": "Ngày sinh",
            "Giới tính": "Giới tính",
            "SDT": "SDT",
            "Email": "Email"
        }
        
        if selected_column in column_map:
            display_columns = [column_map[selected_column], "Tác vụ"]
        else:
            display_columns = all_columns
        
        hidden_columns = [col for col in all_columns if col not in display_columns]
        
        return display_columns, hidden_columns
    
    def search_employees(self, search_text, all_employees):
        """
        Tìm kiếm nhân viên theo từ khóa.
        
        Args:
            search_text (str): Từ khóa tìm kiếm
            all_employees (list): Danh sách tất cả nhân viên
            
        Returns:
            list: Danh sách nhân viên khớp với từ khóa
        """
        search_text = search_text.lower()
        matched = []
        
        for employee in all_employees:
            # Tìm trong các trường: ID, tên, SĐT, email
            if (search_text in str(employee.get('id', '')).lower() or
                search_text in employee.get('full_name', '').lower() or
                search_text in employee.get('phone', '').lower() or
                search_text in employee.get('email', '').lower()):
                matched.append(employee)
        
        return matched
    
    def create_employee(self, employee_data):
        """
        Tạo nhân viên mới qua API.
        
        Args:
            employee_data (dict): Thông tin nhân viên
            
        Returns:
            (success, message, data): Tuple gồm boolean, message và data
        """
        try:
            # TODO: Gọi API để tạo nhân viên
            # response = requests.post(f"{API_URL}/employees", json=employee_data)
            
            # Mock data để test
            new_employee = {
                'id': f"NV{len(self.employees) + 1:03d}",
                **employee_data
            }
            self.employees.append(new_employee)
            
            return True, "Tạo nhân viên thành công!", new_employee
            
        except Exception as e:
            return False, f"Lỗi khi tạo nhân viên: {str(e)}", None
    
    def update_employee(self, employee_id, employee_data):
        """
        Cập nhật thông tin nhân viên qua API.
        
        Args:
            employee_id (str): ID nhân viên
            employee_data (dict): Thông tin cập nhật
            
        Returns:
            (success, message, data): Tuple gồm boolean, message và data
        """
        try:
            # TODO: Gọi API để cập nhật nhân viên
            # response = requests.put(f"{API_URL}/employees/{employee_id}", json=employee_data)
            
            # Mock data để test
            updated_employee = {
                'id': employee_id,
                **employee_data
            }
            
            return True, "Cập nhật nhân viên thành công!", updated_employee
            
        except Exception as e:
            return False, f"Lỗi khi cập nhật nhân viên: {str(e)}", None
    
    def delete_employee(self, employee_id):
        """
        Xóa nhân viên qua API.
        
        Args:
            employee_id (str): ID nhân viên cần xóa
            
        Returns:
            (success, message): Tuple gồm boolean và message
        """
        try:
            # TODO: Gọi API để xóa nhân viên
            # response = requests.delete(f"{API_URL}/employees/{employee_id}")
            
            # Mock data để test
            self.employees = [e for e in self.employees if e.get('id') != employee_id]
            
            return True, "Xóa nhân viên thành công!"
            
        except Exception as e:
            return False, f"Lỗi khi xóa nhân viên: {str(e)}"
