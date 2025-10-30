import customtkinter as ctk
from PIL import Image
from controllers.Employee_Controller import EmployeeController
from gui.Components.Employee_Dialogs_Component import EmployeeDialogs

class EmployeeDetail:
    """Class hiển thị chi tiết thông tin nhân viên."""
    
    def __init__(self, parent):
        """
        Args:
            parent: Component cha (Employee_UI)
        """
        self.parent = parent
        self.controller = EmployeeController()
        self.dialogs = EmployeeDialogs(parent)
    
    # ==================== SHOW EMPLOYEE DETAIL ====================
    
    def show_employee_detail(self, employee_id):
        """Hiển thị popup chi tiết thông tin nhân viên.
        
        Args:
            employee_id (str): ID nhân viên
        """
        # Tạo popup
        popup = ctk.CTkToplevel(self.parent)
        popup.title(f"Chi tiết nhân viên - ID: {employee_id}")
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
            text=f"THÔNG TIN CHI TIẾT NHÂN VIÊN",
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
        
        # TODO: Load avatar từ API nếu có
        # if employee_data.get('avatar'):
        #     try:
        #         image = Image.open(employee_data['avatar'])
        #         image.thumbnail((200, 283), Image.Resampling.LANCZOS)
        #         ctk_image = ctk.CTkImage(light_image=image, size=image.size)
        #         avatar_label.configure(image=ctk_image)
        #     except Exception as e:
        #         avatar_label.configure(text="Không có ảnh")
        
        # ========== RIGHT: FIELDS ==========
        fields_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        fields_frame.grid(row=0, column=1, sticky="nsew", pady=10)
        
        # Dictionary để lưu các entry widgets
        entries = {}
        
        # Danh sách các trường (15 trường)
        fields_config = [
            ("ID", "id", False),
            ("Họ và tên *", "full_name", True),
            ("Ngày sinh *", "birth_date", True),
            ("Giới tính *", "gender", True),
            ("CCCD/CMND *", "citizen_id", True),
            ("SDT *", "phone", True),
            ("Email *", "email", True),
            ("Địa chỉ *", "address", True),
            ("Trình độ", "education", True),
            ("Chức vụ *", "position", True),
            ("Phòng ban *", "department", True),
            ("Ngày bắt đầu làm việc *", "start_date", True),
            ("Trạng thái *", "status", True),
            ("Ghi chú", "note", True),
        ]
        
        # Tạo các trường nhập liệu
        for idx, (label_text, field_name, is_editable) in enumerate(fields_config):
            # Label
            label = ctk.CTkLabel(
                fields_frame,
                text=label_text,
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            label.grid(row=idx, column=0, sticky="w", padx=(10, 10), pady=5)
            
            # Entry hoặc Textbox (cho ghi chú)
            if field_name == "note":
                entry = ctk.CTkTextbox(
                    fields_frame,
                    height=80,
                    font=ctk.CTkFont(size=13),
                    state="disabled",  # Mặc định disabled
                    fg_color="#E8E8E8"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            elif field_name == "gender":
                # Combobox cho giới tính
                entry = ctk.CTkComboBox(
                    fields_frame,
                    values=["Nam", "Nữ", "Khác"],
                    font=ctk.CTkFont(size=13),
                    state="disabled",
                    fg_color="#E8E8E8"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            elif field_name == "status":
                # Combobox cho trạng thái
                entry = ctk.CTkComboBox(
                    fields_frame,
                    values=["Đang làm việc", "Nghỉ việc", "Tạm nghỉ"],
                    font=ctk.CTkFont(size=13),
                    state="disabled",
                    fg_color="#E8E8E8"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            else:
                entry = ctk.CTkEntry(
                    fields_frame,
                    font=ctk.CTkFont(size=13),
                    state="disabled" if field_name == "id" or not is_editable else "normal",
                    fg_color="#E8E8E8" if field_name == "id" else "white"
                )
                entry.grid(row=idx, column=1, sticky="ew", padx=(10, 10), pady=5)
            
            entries[field_name] = entry
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # TODO: Load dữ liệu từ API và fill vào các trường
        # employee_data = self.controller.get_employee_by_id(employee_id)
        # if employee_data:
        #     for field_name, entry in entries.items():
        #         if isinstance(entry, ctk.CTkTextbox):
        #             entry.configure(state="normal")
        #             entry.delete("1.0", "end")
        #             entry.insert("1.0", employee_data.get(field_name, ""))
        #             entry.configure(state="disabled")
        #         elif isinstance(entry, ctk.CTkComboBox):
        #             entry.set(employee_data.get(field_name, ""))
        #         else:
        #             entry.delete(0, "end")
        #             entry.insert(0, employee_data.get(field_name, ""))
        
        # Giả lập dữ liệu mẫu
        sample_data = {
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
            "note": "Nhân viên mẫu mực"
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
                # Chế độ edit: enable các trường (trừ ID)
                edit_button.configure(text="Hủy", fg_color="#F44336", hover_color="#da190b")
                save_button.configure(state="normal")
                
                for field_name, entry in entries.items():
                    if field_name != "id":
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
                
                for field_name, entry in entries.items():
                    if field_name != "id":
                        if isinstance(entry, ctk.CTkTextbox):
                            entry.configure(state="disabled")
                        elif isinstance(entry, ctk.CTkComboBox):
                            entry.configure(state="disabled")
                        else:
                            entry.configure(state="disabled", fg_color="#E8E8E8")
        
        def save_changes():
            """Lưu thay đổi."""
            # Thu thập dữ liệu từ các trường
            employee_data = {}
            for field_name, entry in entries.items():
                if isinstance(entry, ctk.CTkTextbox):
                    employee_data[field_name] = entry.get("1.0", "end-1c").strip()
                elif isinstance(entry, ctk.CTkComboBox):
                    employee_data[field_name] = entry.get()
                else:
                    employee_data[field_name] = entry.get().strip()
            
            # Validate dữ liệu
            is_valid, error_message = self.controller.validate_employee_data(employee_data)
            if not is_valid:
                self.dialogs.show_warning_popup(error_message)
                return
            
            # TODO: Gọi API để update nhân viên
            # success = self.controller.update_employee(employee_id, employee_data)
            # if success:
            #     self.dialogs.show_warning_popup("Cập nhật thành công!")
            #     toggle_edit()  # Quay về chế độ view
            #     self.parent.load_employees()  # Refresh danh sách
            # else:
            #     self.dialogs.show_warning_popup("Cập nhật thất bại!")
            
            # Giả lập cập nhật thành công
            self.dialogs.show_warning_popup("Cập nhật thành công!")
            toggle_edit()
            if hasattr(self.parent, 'load_employees'):
                self.parent.load_employees()
        
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
