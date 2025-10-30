import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from controllers.Account_Forms_Controller import AccountFormsController
from gui.Components.Account_Dialogs_Component import AccountDialogs

class AccountForms:
    """Class chứa các form thêm và sửa tài khoản."""
    
    def __init__(self, parent):
        """
        Args:
            parent: Component cha (Account_UI)
        """
        self.parent = parent
        self.controller = AccountFormsController()
        self.dialogs = AccountDialogs(parent)
        self.avatar_path = None
    
    # ==================== SHOW ADD ACCOUNT FORM ====================
    
    def show_add_account_form(self, on_save_callback):
        """Hiển thị form thêm tài khoản mới.
        
        Args:
            on_save_callback: Callback(account_data, popup) khi nhấn Lưu
        """
        # Tạo popup
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Thêm tài khoản mới")
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
            text="THÊM TÀI KHOẢN MỚI",
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
        
        # Danh sách các trường (8 trường, không có ID, created_at, last_login)
        fields_config = [
            ("Tên đăng nhập *", "username", "entry"),
            ("Mật khẩu *", "password", "password"),
            ("Xác nhận mật khẩu *", "confirm_password", "password"),
            ("Họ và tên *", "full_name", "entry"),
            ("Email *", "email", "entry"),
            ("Số điện thoại", "phone", "entry"),
            ("Vai trò *", "role", "combobox"),
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
            
            # Widget (Entry, Password, Combobox, hoặc Textbox)
            if widget_type == "textbox":
                entry = ctk.CTkTextbox(
                    fields_frame,
                    height=80,
                    font=ctk.CTkFont(size=13),
                    fg_color="white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            elif widget_type == "password":
                entry = ctk.CTkEntry(
                    fields_frame,
                    show="*",
                    font=ctk.CTkFont(size=13),
                    fg_color="white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            elif widget_type == "combobox":
                if field_name == "role":
                    values = ["Admin", "Bác sĩ", "Y tá", "Nhân viên", "Người dùng"]
                elif field_name == "status":
                    values = ["Hoạt động", "Tạm khóa"]
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
        
        def save_account():
            """Lưu tài khoản mới."""
            # Thu thập dữ liệu từ các trường
            account_data = {}
            for field_name, entry in entries.items():
                if isinstance(entry, ctk.CTkTextbox):
                    account_data[field_name] = entry.get("1.0", "end-1c").strip()
                elif isinstance(entry, ctk.CTkComboBox):
                    account_data[field_name] = entry.get()
                else:
                    account_data[field_name] = entry.get().strip()
            
            # Kiểm tra mật khẩu khớp
            if account_data.get("password") != account_data.get("confirm_password"):
                self.dialogs.show_warning_popup("Mật khẩu xác nhận không khớp!")
                return
            
            # Xóa confirm_password khỏi data (không gửi lên API)
            account_data.pop("confirm_password", None)
            
            # Thêm avatar nếu có
            if self.avatar_path:
                account_data["avatar"] = self.avatar_path
            
            # Validate dữ liệu
            is_valid, error_message = self.controller.validate_account_data(account_data, is_edit=False)
            if not is_valid:
                self.dialogs.show_warning_popup(error_message)
                return
            
            # Chuẩn bị dữ liệu cho API
            api_data = self.controller.prepare_api_data(account_data)
            
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
            command=save_account
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
    
    # ==================== SHOW EDIT ACCOUNT FORM ====================
    
    def show_edit_account_form(self, account_id, on_save_callback):
        """Hiển thị form sửa thông tin tài khoản.
        
        Args:
            account_id (str): ID tài khoản
            on_save_callback: Callback(account_data, popup) khi nhấn Lưu
        """
        # TODO: Lấy thông tin tài khoản từ API
        # account_data = self.controller.get_account_by_id(account_id)
        # if not account_data:
        #     self.dialogs.show_warning_popup("Không tìm thấy tài khoản!")
        #     return
        
        # Giả lập dữ liệu mẫu
        account_data = {
            "id": account_id,
            "username": "admin",
            "full_name": "Quản trị viên",
            "email": "admin@example.com",
            "phone": "0123456789",
            "role": "Admin",
            "status": "Hoạt động",
            "note": "Tài khoản quản trị hệ thống",
            "avatar": None
        }
        
        # Tạo popup
        popup = ctk.CTkToplevel(self.parent)
        popup.title(f"Sửa thông tin tài khoản - ID: {account_id}")
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
            text=f"SỬA THÔNG TIN TÀI KHOẢN - ID: {account_id}",
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
        
        # Danh sách các trường (không có password khi edit)
        fields_config = [
            ("Tên đăng nhập", "username", "entry", False),  # Không cho sửa username
            ("Họ và tên *", "full_name", "entry", True),
            ("Email *", "email", "entry", True),
            ("Số điện thoại", "phone", "entry", True),
            ("Vai trò *", "role", "combobox", True),
            ("Trạng thái *", "status", "combobox", True),
            ("Ghi chú", "note", "textbox", True),
        ]
        
        # Tạo các trường nhập liệu và fill dữ liệu
        for idx, (label_text, field_name, widget_type, editable) in enumerate(fields_config):
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
                    fg_color="white" if editable else "#E8E8E8"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
                entry.insert("1.0", account_data.get(field_name, ""))
                if not editable:
                    entry.configure(state="disabled")
            elif widget_type == "combobox":
                if field_name == "role":
                    values = ["Admin", "Bác sĩ", "Y tá", "Nhân viên", "Người dùng"]
                elif field_name == "status":
                    values = ["Hoạt động", "Tạm khóa", "Khóa vĩnh viễn"]
                else:
                    values = []
                
                entry = ctk.CTkComboBox(
                    fields_frame,
                    values=values,
                    font=ctk.CTkFont(size=13),
                    fg_color="white" if editable else "#E8E8E8"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
                entry.set(account_data.get(field_name, values[0] if values else ""))
                if not editable:
                    entry.configure(state="disabled")
            else:
                entry = ctk.CTkEntry(
                    fields_frame,
                    font=ctk.CTkFont(size=13),
                    fg_color="white" if editable else "#E8E8E8"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
                entry.insert(0, account_data.get(field_name, ""))
                if not editable:
                    entry.configure(state="disabled")
            
            entries[field_name] = entry
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # ========== BUTTONS ==========
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=20, padx=20)
        
        def save_changes():
            """Lưu thay đổi."""
            # Thu thập dữ liệu từ các trường
            updated_data = {"id": account_id}
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
            is_valid, error_message = self.controller.validate_account_data(updated_data, is_edit=True)
            if not is_valid:
                self.dialogs.show_warning_popup(error_message)
                return
            
            # Chuẩn bị dữ liệu cho API
            api_data = self.controller.prepare_api_data(updated_data)
            
            # Gọi callback để lưu
            on_save_callback(api_data, popup)
            
            # Reset avatar_path
            self.avatar_path = None
        
        # Nút Lưu thay đổi
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
