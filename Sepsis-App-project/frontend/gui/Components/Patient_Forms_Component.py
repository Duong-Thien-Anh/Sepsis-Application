import customtkinter as ctk
from controllers.Patient_Forms_Controller import PatientFormsController
from gui.Components.Patient_Dialogs_Component import PatientDialogs

class PatientForms:
    """Class chứa các form thêm và sửa bệnh nhân."""
    
    def __init__(self, parent):
        """
        Args:
            parent: Component cha (Patient_UI)
        """
        self.parent = parent
        self.forms_controller = PatientFormsController()
        self.dialogs = PatientDialogs(parent)
    
    # ==================== ADD FORM ====================
    
    def show_add_patient_form(self, on_save_callback):
        """Hiển thị form thêm bệnh nhân mới với giao diện đầy đủ.
        
        Args:
            on_save_callback: Callback(patient_data, popup) khi nhấn nút Lưu
        """
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Thêm bệnh nhân mới")
        popup.geometry("1000x700")
        popup.resizable(False, False)
        
        # Đặt màu nền
        popup.configure(fg_color="#F7F7F5")
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        popup.after(100, lambda: popup.attributes('-topmost', False))
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (1000 // 2)
        y = (popup.winfo_screenheight() // 2) - (700 // 2)
        popup.geometry(f"1000x700+{x}+{y}")

        # Main container
        main_container = ctk.CTkFrame(popup, fg_color="#F7F7F5")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cấu hình grid - 3 rows
        main_container.grid_rowconfigure(0, weight=0)  # Row 0: Tiêu đề
        main_container.grid_rowconfigure(1, weight=1)  # Row 1: Nội dung chính (Avatar + Fields)
        main_container.grid_rowconfigure(2, weight=0)  # Row 2: Buttons
        main_container.grid_columnconfigure(0, weight=1)
        
        # ==================== ROW 0: TIÊU ĐỀ ====================
        title_frame = ctk.CTkFrame(main_container, fg_color="#4CAF50", corner_radius=8, border_width=2, border_color="black")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="➕ THÊM BỆNH NHÂN MỚI",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=15)
        
        # ==================== ROW 1: NỘI DUNG CHÍNH (2 COLUMNS) ====================
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        
        # Cấu hình grid cho content_frame (2 columns)
        content_frame.grid_columnconfigure(0, weight=0)  # Column 0: Avatar (200px fixed)
        content_frame.grid_columnconfigure(1, weight=1)  # Column 1: Fields với scrollbar
        content_frame.grid_rowconfigure(0, weight=1)
        
        # --- COLUMN 0: Avatar Frame (200x283px) + Upload Button ---
        avatar_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        avatar_container.grid(row=0, column=0, sticky="n", padx=(0, 20))
        
        # Avatar Frame với viền màu
        avatar_frame = ctk.CTkFrame(
            avatar_container,
            fg_color="#E0E0E0",
            corner_radius=8,
            width=200,
            height=283,
            border_width=3,
            border_color="#4CAF50"
        )
        avatar_frame.pack()
        avatar_frame.pack_propagate(False)
        
        # Label hiển thị ảnh
        avatar_image_label = ctk.CTkLabel(
            avatar_frame,
            text="👤\nChưa có ảnh",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#757575"
        )
        avatar_image_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Lưu reference ảnh
        avatar_photo = [None]
        
        # Text "Ảnh đại diện"
        avatar_text = ctk.CTkLabel(
            avatar_container,
            text="Ảnh đại diện",
            font=ctk.CTkFont(size=12),
            text_color="#757575"
        )
        avatar_text.pack(pady=(5, 10))
        
        # Nút tải ảnh
        def upload_avatar():
            """Mở hộp thoại chọn ảnh"""
            def on_success(image, file_path):
                # Chuyển đổi sang CTkImage
                ctk_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(image.width, image.height)
                )
                avatar_image_label.configure(image=ctk_image, text="")
                avatar_photo[0] = ctk_image
            
            def on_error(error_msg):
                self.dialogs.show_warning_popup(error_msg)
            
            self.forms_controller.upload_avatar(
                avatar_image_label,
                on_success_callback=on_success,
                on_error_callback=on_error
            )
        
        upload_btn = ctk.CTkButton(
            avatar_container,
            text="📤 Tải ảnh lên",
            width=200,
            height=35,
            corner_radius=8,
            fg_color="#2196F3",
            hover_color="#1976D2",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=upload_avatar
        )
        upload_btn.pack()
        
        # --- COLUMN 1: Scrollable Frame chứa các Input Fields ---
        scrollable_frame = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="transparent",
            scrollbar_button_color="#4CAF50",
            scrollbar_button_hover_color="#45a049"
        )
        scrollable_frame.grid(row=0, column=1, sticky="nsew")
        
        # Dictionary lưu các entry fields
        entry_fields = {}
        
        # Danh sách 14 fields (không có ID vì đang thêm mới)
        info_fields = [
            ("Họ và tên:", "", "họ_và_tên", "entry", True),
            ("Ngày sinh:", "DD/MM/YYYY", "ngày_sinh", "entry", True),
            ("Giới tính:", "Nam", "giới_tính", "option", True),
            ("Số điện thoại:", "0901234567", "số_điện_thoại", "entry", True),
            ("Email:", "example@email.com", "email", "entry", False),
            ("Địa chỉ:", "", "địa_chỉ", "entry", False),
            ("Chức vụ:", "", "chức_vụ", "entry", False),
            ("Ngày bắt đầu làm việc:", "DD/MM/YYYY", "ngày_bắt_đầu_làm_việc", "entry", False),
            ("Cân nặng (kg):", "", "cân_nặng_(kg)", "entry", False),
            ("Tiểu sử bệnh lý:", "", "tiểu_sử_bệnh_lý", "textbox", False),
            ("Tên người thân:", "", "tên_người_thân", "entry", False),
            ("Số điện thoại người thân:", "", "số_điện_thoại_người_thân", "entry", False),
            ("Quan hệ người thân:", "", "quan_hệ_người_thân", "entry", False),
            ("Ghi chú:", "", "ghi_chú", "textbox", False),
        ]
        
        # Tạo các input fields
        for label_text, placeholder, field_key, field_type, is_required in info_fields:
            # Frame cho mỗi field
            field_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=8, padx=5)
            
            # Label với dấu * nếu bắt buộc
            label_display = label_text + " *" if is_required else label_text
            label = ctk.CTkLabel(
                field_frame,
                text=label_display,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="red" if is_required else "black",
                anchor="w",
                width=200
            )
            label.pack(side="left", padx=(0, 15))
            
            # Tạo widget tùy theo loại
            if field_type == "textbox":
                # CTkTextbox cho trường dài
                entry = ctk.CTkTextbox(
                    field_frame,
                    height=80,
                    font=ctk.CTkFont(size=13),
                    wrap="word"
                )
                entry.pack(side="left", fill="x", expand=True)
            elif field_type == "option":
                # CTkOptionMenu cho giới tính
                entry = ctk.CTkOptionMenu(
                    field_frame,
                    values=["Nam", "Nữ"],
                    height=35,
                    font=ctk.CTkFont(size=13)
                )
                entry.set(placeholder)
                entry.pack(side="left", fill="x", expand=True)
            else:
                # CTkEntry cho trường thông thường
                entry = ctk.CTkEntry(
                    field_frame,
                    height=35,
                    font=ctk.CTkFont(size=13),
                    placeholder_text=placeholder
                )
                entry.pack(side="left", fill="x", expand=True)
            
            entry_fields[field_key] = entry
        
        # ==================== ROW 2: BUTTONS ====================
        button_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew")
        
        # Căn giữa các button
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_frame.grid_columnconfigure(3, weight=1)
        
        def save_patient():
            """Xử lý khi nhấn nút Lưu"""
            # Validate dữ liệu
            is_valid, error_msg, patient_data = self.forms_controller.validate_patient_data(entry_fields)
            
            if not is_valid:
                self.dialogs.show_warning_popup(error_msg)
                return
            
            # Chuẩn bị dữ liệu cho API
            api_data = self.forms_controller.prepare_api_data(patient_data)
            
            # Gọi callback
            on_save_callback(api_data, popup)
        
        # Nút Hủy
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Hủy",
            width=200,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#F44336",
            hover_color="#da190b",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=popup.destroy
        )
        cancel_btn.grid(row=0, column=1, padx=10)
        
        # Nút Lưu
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Lưu",
            width=200,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=save_patient
        )
        save_btn.grid(row=0, column=2, padx=10)
    
    # ==================== EDIT FORM ====================
    
    def show_edit_patient_form(self, patient_data, on_save_callback):
        """Hiển thị form chỉnh sửa bệnh nhân.
        
        Args:
            patient_data (tuple): (STT, ID, Họ tên, Ngày sinh, Giới tính, SDT, Email)
            on_save_callback: Callback(patient_id, fields_dict, popup) khi nhấn nút Lưu
        """
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Chỉnh sửa bệnh nhân")
        popup.geometry("500x600")
        popup.resizable(False, False)
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        popup.after(100, lambda: popup.attributes('-topmost', False))
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (500 // 2)
        y = (popup.winfo_screenheight() // 2) - (600 // 2)
        popup.geometry(f"500x600+{x}+{y}")
        
        # Header
        header = ctk.CTkFrame(popup, fg_color="#FFA726", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="✏️ CHỈNH SỬA BỆNH NHÂN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title.pack(pady=15)
        
        # Content
        content = ctk.CTkFrame(popup, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Fields
        fields = {}
        patient_id = patient_data[1]  # Lưu ID để update
        
        # Họ và tên
        ctk.CTkLabel(content, text="Họ và tên:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['full_name'] = ctk.CTkEntry(content, height=40, font=ctk.CTkFont(size=13))
        fields['full_name'].insert(0, patient_data[2])
        fields['full_name'].pack(fill="x", pady=(0,10))
        
        # Ngày sinh
        ctk.CTkLabel(content, text="Ngày sinh (DD/MM/YYYY):", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['birth_date'] = ctk.CTkEntry(content, height=40, font=ctk.CTkFont(size=13))
        fields['birth_date'].insert(0, patient_data[3])
        fields['birth_date'].pack(fill="x", pady=(0,10))
        
        # Giới tính
        ctk.CTkLabel(content, text="Giới tính:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['gender'] = ctk.CTkOptionMenu(content, values=["Nam", "Nữ"], height=40, font=ctk.CTkFont(size=13))
        fields['gender'].set(patient_data[4])
        fields['gender'].pack(fill="x", pady=(0,10))
        
        # Số điện thoại
        ctk.CTkLabel(content, text="Số điện thoại:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['phone'] = ctk.CTkEntry(content, height=40, font=ctk.CTkFont(size=13))
        fields['phone'].insert(0, patient_data[5])
        fields['phone'].pack(fill="x", pady=(0,10))
        
        # Email
        ctk.CTkLabel(content, text="Email:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['email'] = ctk.CTkEntry(content, height=40, font=ctk.CTkFont(size=13))
        fields['email'].insert(0, patient_data[6])
        fields['email'].pack(fill="x", pady=(0,10))
        
        # Footer buttons
        footer = ctk.CTkFrame(popup, fg_color="transparent")
        footer.pack(fill="x", padx=30, pady=(0, 20))
        
        # Nút Lưu
        save_btn = ctk.CTkButton(
            footer,
            text="💾 Lưu",
            width=220,
            height=42,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#FFA726",
            hover_color="#FB8C00",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: on_save_callback(patient_id, fields, popup)
        )
        save_btn.pack(side="left", padx=5)
        
        # Nút Hủy
        cancel_btn = ctk.CTkButton(
            footer,
            text="❌ Hủy",
            width=220,
            height=42,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#F44336",
            hover_color="#da190b",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=popup.destroy
        )
        cancel_btn.pack(side="left", padx=5)
