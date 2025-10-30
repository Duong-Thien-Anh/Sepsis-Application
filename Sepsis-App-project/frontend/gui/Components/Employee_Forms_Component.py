import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from controllers.Employee_Forms_Controller import EmployeeFormsController
from gui.Components.Employee_Dialogs_Component import EmployeeDialogs

class EmployeeForms:
    """Class chứa các form thêm và sửa nhân viên."""
    
    def __init__(self, parent):
        """
        Args:
            parent: Component cha (Employee_UI)
        """
        self.parent = parent
        self.controller = EmployeeFormsController()
        self.dialogs = EmployeeDialogs(parent)
        self.avatar_path = None
    
    # ==================== SHOW ADD EMPLOYEE FORM ====================
    
    def show_add_employee_form(self, on_save_callback):
        """Hiển thị form thêm nhân viên mới.
        
        Args:
            on_save_callback: Callback(employee_data, popup) khi nhấn Lưu
        """
        # Tạo popup
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Thêm nhân viên mới")
        popup.geometry("1000x700")
        popup.resizable(False, False)
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (1000 // 2)
        y = (popup.winfo_screenheight() // 2) - (700 // 2)
        popup.geometry(f"1000x700+{x}+{y}")
        
        # Grid configuration
        popup.grid_rowconfigure(0, weight=0)  # Header
        popup.grid_rowconfigure(1, weight=1)  # Content
        popup.grid_rowconfigure(2, weight=0)  # Buttons
        popup.grid_columnconfigure(0, weight=1)
        
        # ========== HEADER ==========
        header = ctk.CTkLabel(
            popup,
            text="THÊM NHÂN VIÊN MỚI",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4CAF50"
        )
        header.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        
        # ========== CONTENT FRAME (scrollable) ==========
        content_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color="transparent",
            scrollbar_button_color="#4CAF50",
            scrollbar_button_hover_color="#45a049"
        )
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        content_frame.grid_columnconfigure(0, weight=0)  # Avatar column
        content_frame.grid_columnconfigure(1, weight=1)  # Fields column
        
        # ========== LEFT: AVATAR ==========
        avatar_frame = ctk.CTkFrame(
            content_frame,
            width=200,
            height=283,
            fg_color="#E8E8E8",
            border_width=3,
            border_color="#4CAF50"
        )
        avatar_frame.grid(row=0, column=0, padx=(10, 20), pady=10, sticky="n")
        avatar_frame.grid_propagate(False)
        
        # Label hiển thị avatar
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="Chưa có ảnh",
            fg_color="transparent"
        )
        avatar_label.place(relx=0.5, rely=0.4, anchor="center")
        
        # Nút upload avatar
        upload_button = ctk.CTkButton(
            avatar_frame,
            text="📷 Tải ảnh lên",
            width=150,
            height=35,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=lambda: self.controller.upload_avatar(avatar_label, self)
        )
        upload_button.place(relx=0.5, rely=0.7, anchor="center")
        
        # ========== RIGHT: FIELDS ==========
        fields_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        fields_frame.grid(row=0, column=1, sticky="nsew", pady=10)
        
        # Dictionary để lưu các entry widgets
        entries = {}
        
        # Danh sách các trường (14 trường, không có ID)
        fields_config = [
            ("Họ và tên *", "full_name", "entry"),
            ("Ngày sinh *", "birth_date", "entry"),
            ("Giới tính *", "gender", "combobox"),
            ("CCCD/CMND *", "citizen_id", "entry"),
            ("SDT *", "phone", "entry"),
            ("Email *", "email", "entry"),
            ("Địa chỉ *", "address", "entry"),
            ("Trình độ", "education", "entry"),
            ("Chức vụ *", "position", "entry"),
            ("Phòng ban *", "department", "entry"),
            ("Ngày bắt đầu làm việc *", "start_date", "entry"),
            ("Trạng thái *", "status", "combobox"),
            ("Ghi chú", "note", "textbox"),
        ]
        
        # Tạo các trường nhập liệu
        for idx, (label_text, field_name, widget_type) in enumerate(fields_config):
            # Label
            label = ctk.CTkLabel(
                fields_frame,
                text=label_text,
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            label.grid(row=idx, column=0, sticky="w", padx=(10, 10), pady=5)
            
            # Widget (Entry, Combobox, hoặc Textbox)
            if widget_type == "textbox":
                entry = ctk.CTkTextbox(
                    fields_frame,
                    height=80,
                    font=ctk.CTkFont(size=13),
                    fg_color="white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            elif widget_type == "combobox":
                if field_name == "gender":
                    values = ["Nam", "Nữ", "Khác"]
                elif field_name == "status":
                    values = ["Đang làm việc", "Nghỉ việc", "Tạm nghỉ"]
                else:
                    values = []
                
                entry = ctk.CTkComboBox(
                    fields_frame,
                    values=values,
                    font=ctk.CTkFont(size=13),
                    fg_color="white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
                if values:
                    entry.set(values[0])  # Set giá trị mặc định
            else:
                entry = ctk.CTkEntry(
                    fields_frame,
                    font=ctk.CTkFont(size=13),
                    fg_color="white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            
            entries[field_name] = entry
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # ========== BUTTONS ==========
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=20, padx=20)
        
        def save_employee():
            """Lưu nhân viên mới."""
            # Thu thập dữ liệu từ các trường
            employee_data = {}
            for field_name, entry in entries.items():
                if isinstance(entry, ctk.CTkTextbox):
                    employee_data[field_name] = entry.get("1.0", "end-1c").strip()
                elif isinstance(entry, ctk.CTkComboBox):
                    employee_data[field_name] = entry.get()
                else:
                    employee_data[field_name] = entry.get().strip()
            
            # Thêm avatar nếu có
            if self.avatar_path:
                employee_data["avatar"] = self.avatar_path
            
            # Validate dữ liệu
            is_valid, error_message = self.controller.validate_employee_data(employee_data)
            if not is_valid:
                self.dialogs.show_warning_popup(error_message)
                return
            
            # Chuẩn bị dữ liệu cho API
            api_data = self.controller.prepare_api_data(employee_data)
            
            # Gọi callback để lưu
            on_save_callback(api_data, popup)
            
            # Reset avatar_path
            self.avatar_path = None
        
        # Nút Lưu
        save_button = ctk.CTkButton(
            button_frame,
            text="💾 Lưu",
            width=120,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=save_employee
        )
        save_button.pack(side="left", padx=10)
        
        # Nút Hủy
        cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ Hủy",
            width=120,
            height=40,
            fg_color="#F44336",
            hover_color="#da190b",
            command=popup.destroy
        )
        cancel_button.pack(side="left", padx=10)
    
    # ==================== SHOW EDIT EMPLOYEE FORM ====================
    
    def show_edit_employee_form(self, employee_id, on_save_callback):
        """Hiển thị form sửa thông tin nhân viên.
        
        Args:
            employee_id (str): ID nhân viên
            on_save_callback: Callback(employee_data, popup) khi nhấn Lưu
        """
        # TODO: Lấy thông tin nhân viên từ API
        # employee_data = self.controller.get_employee_by_id(employee_id)
        # if not employee_data:
        #     self.dialogs.show_warning_popup("Không tìm thấy nhân viên!")
        #     return
        
        # Giả lập dữ liệu mẫu
        employee_data = {
            "id": employee_id,
            "full_name": "Nguyễn Văn A",
            "birth_date": "01/01/1990",
            "gender": "Nam",
            "citizen_id": "001234567890",
            "phone": "0123456789",
            "email": "nguyenvana@example.com",
            "address": "123 Đường ABC, Quận 1, TP.HCM",
            "education": "Đại học",
            "position": "Nhân viên",
            "department": "Phòng Kỹ thuật",
            "start_date": "01/01/2020",
            "status": "Đang làm việc",
            "note": "Nhân viên mẫu mực",
            "avatar": None
        }
        
        # Tạo popup
        popup = ctk.CTkToplevel(self.parent)
        popup.title(f"Sửa thông tin nhân viên - ID: {employee_id}")
        popup.geometry("1000x700")
        popup.resizable(False, False)
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (1000 // 2)
        y = (popup.winfo_screenheight() // 2) - (700 // 2)
        popup.geometry(f"1000x700+{x}+{y}")
        
        # Grid configuration
        popup.grid_rowconfigure(0, weight=0)  # Header
        popup.grid_rowconfigure(1, weight=1)  # Content
        popup.grid_rowconfigure(2, weight=0)  # Buttons
        popup.grid_columnconfigure(0, weight=1)
        
        # ========== HEADER ==========
        header = ctk.CTkLabel(
            popup,
            text=f"SỬA THÔNG TIN NHÂN VIÊN - ID: {employee_id}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2196F3"
        )
        header.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        
        # ========== CONTENT FRAME (scrollable) ==========
        content_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color="transparent",
            scrollbar_button_color="#2196F3",
            scrollbar_button_hover_color="#0b7dda"
        )
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        content_frame.grid_columnconfigure(0, weight=0)  # Avatar column
        content_frame.grid_columnconfigure(1, weight=1)  # Fields column
        
        # ========== LEFT: AVATAR ==========
        avatar_frame = ctk.CTkFrame(
            content_frame,
            width=200,
            height=283,
            fg_color="#E8E8E8",
            border_width=3,
            border_color="#2196F3"
        )
        avatar_frame.grid(row=0, column=0, padx=(10, 20), pady=10, sticky="n")
        avatar_frame.grid_propagate(False)
        
        # Label hiển thị avatar
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="Chưa có ảnh",
            fg_color="transparent"
        )
        avatar_label.place(relx=0.5, rely=0.4, anchor="center")
        
        # TODO: Load avatar từ employee_data
        # if employee_data.get("avatar"):
        #     try:
        #         image = Image.open(employee_data["avatar"])
        #         image.thumbnail((200, 283), Image.Resampling.LANCZOS)
        #         ctk_image = ctk.CTkImage(light_image=image, size=image.size)
        #         avatar_label.configure(image=ctk_image, text="")
        #         self.avatar_path = employee_data["avatar"]
        #     except Exception as e:
        #         avatar_label.configure(text="Lỗi tải ảnh")
        
        # Nút upload avatar
        upload_button = ctk.CTkButton(
            avatar_frame,
            text="📷 Đổi ảnh",
            width=150,
            height=35,
            fg_color="#2196F3",
            hover_color="#0b7dda",
            command=lambda: self.controller.upload_avatar(avatar_label, self)
        )
        upload_button.place(relx=0.5, rely=0.7, anchor="center")
        
        # ========== RIGHT: FIELDS ==========
        fields_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        fields_frame.grid(row=0, column=1, sticky="nsew", pady=10)
        
        # Dictionary để lưu các entry widgets
        entries = {}
        
        # Danh sách các trường (14 trường, không có ID)
        fields_config = [
            ("Họ và tên *", "full_name", "entry"),
            ("Ngày sinh *", "birth_date", "entry"),
            ("Giới tính *", "gender", "combobox"),
            ("CCCD/CMND *", "citizen_id", "entry"),
            ("SDT *", "phone", "entry"),
            ("Email *", "email", "entry"),
            ("Địa chỉ *", "address", "entry"),
            ("Trình độ", "education", "entry"),
            ("Chức vụ *", "position", "entry"),
            ("Phòng ban *", "department", "entry"),
            ("Ngày bắt đầu làm việc *", "start_date", "entry"),
            ("Trạng thái *", "status", "combobox"),
            ("Ghi chú", "note", "textbox"),
        ]
        
        # Tạo các trường nhập liệu và fill dữ liệu
        for idx, (label_text, field_name, widget_type) in enumerate(fields_config):
            # Label
            label = ctk.CTkLabel(
                fields_frame,
                text=label_text,
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            label.grid(row=idx, column=0, sticky="w", padx=(10, 10), pady=5)
            
            # Widget (Entry, Combobox, hoặc Textbox)
            if widget_type == "textbox":
                entry = ctk.CTkTextbox(
                    fields_frame,
                    height=80,
                    font=ctk.CTkFont(size=13),
                    fg_color="white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
                entry.insert("1.0", employee_data.get(field_name, ""))
            elif widget_type == "combobox":
                if field_name == "gender":
                    values = ["Nam", "Nữ", "Khác"]
                elif field_name == "status":
                    values = ["Đang làm việc", "Nghỉ việc", "Tạm nghỉ"]
                else:
                    values = []
                
                entry = ctk.CTkComboBox(
                    fields_frame,
                    values=values,
                    font=ctk.CTkFont(size=13),
                    fg_color="white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
                entry.set(employee_data.get(field_name, values[0] if values else ""))
            else:
                entry = ctk.CTkEntry(
                    fields_frame,
                    font=ctk.CTkFont(size=13),
                    fg_color="white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
                entry.insert(0, employee_data.get(field_name, ""))
            
            entries[field_name] = entry
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # ========== BUTTONS ==========
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=20, padx=20)
        
        def save_changes():
            """Lưu thay đổi."""
            # Thu thập dữ liệu từ các trường
            updated_data = {"id": employee_id}
            for field_name, entry in entries.items():
                if isinstance(entry, ctk.CTkTextbox):
                    updated_data[field_name] = entry.get("1.0", "end-1c").strip()
                elif isinstance(entry, ctk.CTkComboBox):
                    updated_data[field_name] = entry.get()
                else:
                    updated_data[field_name] = entry.get().strip()
            
            # Thêm avatar nếu có
            if self.avatar_path:
                updated_data["avatar"] = self.avatar_path
            
            # Validate dữ liệu
            is_valid, error_message = self.controller.validate_employee_data(updated_data)
            if not is_valid:
                self.dialogs.show_warning_popup(error_message)
                return
            
            # Chuẩn bị dữ liệu cho API
            api_data = self.controller.prepare_api_data(updated_data)
            
            # Gọi callback để lưu
            on_save_callback(api_data, popup)
            
            # Reset avatar_path
            self.avatar_path = None
        
        # Nút Lưu
        save_button = ctk.CTkButton(
            button_frame,
            text="💾 Lưu thay đổi",
            width=140,
            height=40,
            fg_color="#2196F3",
            hover_color="#0b7dda",
            command=save_changes
        )
        save_button.pack(side="left", padx=10)
        
        # Nút Hủy
        cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ Hủy",
            width=120,
            height=40,
            fg_color="#F44336",
            hover_color="#da190b",
            command=popup.destroy
        )
        cancel_button.pack(side="left", padx=10)
