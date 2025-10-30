import customtkinter as ctk
from PIL import Image
from controllers.Account_Controller import AccountController
from gui.Components.Account_Dialogs_Component import AccountDialogs

class AccountDetail:
    """Class hiển thị chi tiết thông tin tài khoản."""
    
    def __init__(self, parent):
        """
        Args:
            parent: Component cha (Account_UI)
        """
        self.parent = parent
        self.controller = AccountController()
        self.dialogs = AccountDialogs(parent)
    
    # ==================== SHOW ACCOUNT DETAIL ====================
    
    def show_account_detail(self, account_id):
        """Hiển thị popup chi tiết thông tin tài khoản.
        
        Args:
            account_id (str): ID tài khoản
        """
        # Tạo popup
        popup = ctk.CTkToplevel(self.parent)
        popup.title(f"Chi tiết tài khoản - ID: {account_id}")
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
            text=f"THÔNG TIN CHI TIẾT TÀI KHOẢN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#66B7FF"
        )
        header.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        
        # ========== CONTENT FRAME (scrollable) ==========
        content_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color="transparent",
            scrollbar_button_color="#66B7FF",
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
            border_color="#66B7FF"
        )
        avatar_frame.grid(row=0, column=0, padx=(10, 20), pady=10, sticky="n")
        avatar_frame.grid_propagate(False)
        
        # Placeholder cho avatar (sẽ load từ API)
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="",
            fg_color="transparent"
        )
        avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # ========== RIGHT: FIELDS ==========
        fields_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        fields_frame.grid(row=0, column=1, sticky="nsew", pady=10)
        
        # Dictionary để lưu các entry widgets
        entries = {}
        
        # Danh sách các trường (10 trường)
        fields_config = [
            ("ID", "id", False, "entry"),
            ("Tên đăng nhập *", "username", True, "entry"),
            ("Họ và tên *", "full_name", True, "entry"),
            ("Email *", "email", True, "entry"),
            ("Số điện thoại", "phone", True, "entry"),
            ("Vai trò *", "role", True, "combobox"),
            ("Trạng thái *", "status", True, "combobox"),
            ("Ngày tạo", "created_at", False, "entry"),
            ("Lần đăng nhập cuối", "last_login", False, "entry"),
            ("Ghi chú", "note", True, "textbox"),
        ]
        
        # Tạo các trường nhập liệu
        for idx, (label_text, field_name, is_editable, widget_type) in enumerate(fields_config):
            # Label
            label = ctk.CTkLabel(
                fields_frame,
                text=label_text,
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            label.grid(row=idx, column=0, sticky="w", padx=(10, 10), pady=5)
            
            # Entry hoặc Textbox (cho ghi chú)
            if widget_type == "textbox":
                entry = ctk.CTkTextbox(
                    fields_frame,
                    height=80,
                    font=ctk.CTkFont(size=13),
                    state="disabled",  # Mặc định disabled
                    fg_color="#E8E8E8"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
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
                    state="disabled",
                    fg_color="#E8E8E8"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            else:
                entry = ctk.CTkEntry(
                    fields_frame,
                    font=ctk.CTkFont(size=13),
                    state="disabled" if not is_editable else "normal",
                    fg_color="#E8E8E8" if not is_editable else "white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            
            entries[field_name] = entry
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # Giả lập dữ liệu mẫu
        sample_data = {
            "id": account_id,
            "username": "admin",
            "full_name": "Quản trị viên",
            "email": "admin@example.com",
            "phone": "0123456789",
            "role": "Admin",
            "status": "Hoạt động",
            "created_at": "01/01/2024",
            "last_login": "30/10/2025 10:30:00",
            "note": "Tài khoản quản trị hệ thống"
        }
        
        for field_name, value in sample_data.items():
            entry = entries[field_name]
            if isinstance(entry, ctk.CTkTextbox):
                entry.configure(state="normal")
                entry.delete("1.0", "end")
                entry.insert("1.0", value)
                entry.configure(state="disabled")
            elif isinstance(entry, ctk.CTkComboBox):
                entry.set(value)
            else:
                if entry.cget("state") == "normal":
                    entry.delete(0, "end")
                    entry.insert(0, value)
                else:
                    entry.configure(state="normal")
                    entry.delete(0, "end")
                    entry.insert(0, value)
                    entry.configure(state="disabled")
        
        # ========== BUTTONS ==========
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=20, padx=20)
        
        # Biến để theo dõi trạng thái edit
        is_editing = {"value": False}
        
        def toggle_edit():
            """Toggle giữa chế độ xem và chỉnh sửa."""
            is_editing["value"] = not is_editing["value"]
            
            if is_editing["value"]:
                # Chế độ edit: enable các trường (trừ ID, username, created_at, last_login)
                edit_button.configure(text="Hủy", fg_color="#F44336", hover_color="#da190b")
                save_button.configure(state="normal")
                change_password_button.configure(state="normal")
                
                non_editable = ["id", "username", "created_at", "last_login"]
                for field_name, entry in entries.items():
                    if field_name not in non_editable:
                        if isinstance(entry, ctk.CTkTextbox):
                            entry.configure(state="normal")
                        elif isinstance(entry, ctk.CTkComboBox):
                            entry.configure(state="readonly")
                        else:
                            entry.configure(state="normal", fg_color="white")
            else:
                # Chế độ view: disable các trường
                edit_button.configure(text="Sửa", fg_color="#4CAF50", hover_color="#45a049")
                save_button.configure(state="disabled")
                change_password_button.configure(state="disabled")
                
                for field_name, entry in entries.items():
                    if field_name not in ["id", "username", "created_at", "last_login"]:
                        if isinstance(entry, ctk.CTkTextbox):
                            entry.configure(state="disabled")
                        elif isinstance(entry, ctk.CTkComboBox):
                            entry.configure(state="disabled")
                        else:
                            entry.configure(state="disabled", fg_color="#E8E8E8")
        
        def save_changes():
            """Lưu thay đổi."""
            # Thu thập dữ liệu từ các trường
            account_data = {}
            for field_name, entry in entries.items():
                if isinstance(entry, ctk.CTkTextbox):
                    account_data[field_name] = entry.get("1.0", "end-1c").strip()
                elif isinstance(entry, ctk.CTkComboBox):
                    account_data[field_name] = entry.get()
                else:
                    account_data[field_name] = entry.get().strip()
            
            # Validate dữ liệu
            is_valid, error_message = self.controller.validate_account_data(account_data, is_edit=True)
            if not is_valid:
                self.dialogs.show_warning_popup(error_message)
                return
            
            # TODO: Gọi API để update tài khoản
            # Giả lập cập nhật thành công
            self.dialogs.show_warning_popup("Cập nhật thành công!")
            toggle_edit()
            if hasattr(self.parent, 'load_accounts'):
                self.parent.load_accounts()
        
        def change_password():
            """Mở popup đổi mật khẩu."""
            self.show_change_password_popup(account_id)
        
        # Nút Sửa/Hủy
        edit_button = ctk.CTkButton(
            button_frame,
            text="Sửa",
            width=120,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=toggle_edit
        )
        edit_button.pack(side="left", padx=10)
        
        # Nút Lưu
        save_button = ctk.CTkButton(
            button_frame,
            text="Lưu",
            width=120,
            height=40,
            fg_color="#2196F3",
            hover_color="#0b7dda",
            state="disabled",
            command=save_changes
        )
        save_button.pack(side="left", padx=10)
        
        # Nút Đổi mật khẩu
        change_password_button = ctk.CTkButton(
            button_frame,
            text="Đổi mật khẩu",
            width=130,
            height=40,
            fg_color="#FF9800",
            hover_color="#F57C00",
            state="disabled",
            command=change_password
        )
        change_password_button.pack(side="left", padx=10)
        
        # Nút Đóng
        close_button = ctk.CTkButton(
            button_frame,
            text="Đóng",
            width=120,
            height=40,
            fg_color="#666666",
            hover_color="#555555",
            command=popup.destroy
        )
        close_button.pack(side="left", padx=10)
    
    # ==================== CHANGE PASSWORD POPUP ====================
    
    def show_change_password_popup(self, account_id):
        """Hiển thị popup đổi mật khẩu.
        
        Args:
            account_id (str): ID tài khoản
        """
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Đổi mật khẩu")
        popup.geometry("400x300")
        popup.resizable(False, False)
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (400 // 2)
        y = (popup.winfo_screenheight() // 2) - (300 // 2)
        popup.geometry(f"400x300+{x}+{y}")
        
        # Header
        header = ctk.CTkLabel(
            popup,
            text="ĐỔI MẬT KHẨU",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF9800"
        )
        header.pack(pady=20)
        
        # Frame chứa các trường
        fields_frame = ctk.CTkFrame(popup, fg_color="transparent")
        fields_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Mật khẩu cũ
        old_password_label = ctk.CTkLabel(fields_frame, text="Mật khẩu cũ:", font=ctk.CTkFont(size=13))
        old_password_label.pack(anchor="w", pady=(10, 5))
        old_password_entry = ctk.CTkEntry(fields_frame, show="*", font=ctk.CTkFont(size=13))
        old_password_entry.pack(fill="x", pady=(0, 10))
        
        # Mật khẩu mới
        new_password_label = ctk.CTkLabel(fields_frame, text="Mật khẩu mới:", font=ctk.CTkFont(size=13))
        new_password_label.pack(anchor="w", pady=(10, 5))
        new_password_entry = ctk.CTkEntry(fields_frame, show="*", font=ctk.CTkFont(size=13))
        new_password_entry.pack(fill="x", pady=(0, 10))
        
        # Xác nhận mật khẩu mới
        confirm_password_label = ctk.CTkLabel(fields_frame, text="Xác nhận mật khẩu mới:", font=ctk.CTkFont(size=13))
        confirm_password_label.pack(anchor="w", pady=(10, 5))
        confirm_password_entry = ctk.CTkEntry(fields_frame, show="*", font=ctk.CTkFont(size=13))
        confirm_password_entry.pack(fill="x", pady=(0, 10))
        
        # Buttons
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def submit_change_password():
            """Xử lý đổi mật khẩu."""
            old_pass = old_password_entry.get().strip()
            new_pass = new_password_entry.get().strip()
            confirm_pass = confirm_password_entry.get().strip()
            
            if not old_pass or not new_pass or not confirm_pass:
                self.dialogs.show_warning_popup("Vui lòng nhập đầy đủ thông tin!")
                return
            
            if new_pass != confirm_pass:
                self.dialogs.show_warning_popup("Mật khẩu mới không khớp!")
                return
            
            if len(new_pass) < 6:
                self.dialogs.show_warning_popup("Mật khẩu mới phải có ít nhất 6 ký tự!")
                return
            
            # TODO: Gọi API để đổi mật khẩu
            # success, message = self.controller.change_password(account_id, old_pass, new_pass)
            # if success:
            #     popup.destroy()
            #     self.dialogs.show_warning_popup(message)
            
            # Giả lập thành công
            popup.destroy()
            self.dialogs.show_warning_popup("Đổi mật khẩu thành công!")
        
        # Nút Xác nhận
        submit_button = ctk.CTkButton(
            button_frame,
            text="Xác nhận",
            width=120,
            height=35,
            fg_color="#FF9800",
            hover_color="#F57C00",
            command=submit_change_password
        )
        submit_button.pack(side="left", padx=10)
        
        # Nút Hủy
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Hủy",
            width=120,
            height=35,
            fg_color="#666666",
            hover_color="#555555",
            command=popup.destroy
        )
        cancel_button.pack(side="left", padx=10)
