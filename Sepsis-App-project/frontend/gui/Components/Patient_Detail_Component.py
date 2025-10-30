import customtkinter as ctk
from controllers.Patient_Detail_Controller import PatientDetailController
from gui.Components.Patient_Dialogs_Component import PatientDialogs

class PatientDetail:
    """Class chứa popup hiển thị chi tiết bệnh nhân."""
    
    def __init__(self, parent):
        """
        Args:
            parent: Component cha (Patient_UI)
        """
        self.parent = parent
        self.detail_controller = PatientDetailController()  # Controller cho detail popup
        self.dialogs = PatientDialogs(parent)  # Dialog để hiển thị cảnh báo
    
    # ==================== DETAIL POPUP ====================
    
    def show_patient_detail(self, patient_data, on_edit_callback, on_delete_callback):
        """Hiển thị popup chi tiết bệnh nhân.
        
        Args:
            patient_data (tuple): (STT, ID, Họ tên, Ngày sinh, Giới tính, SDT, Email, ...)
            on_edit_callback: Callback khi nhấn nút Sửa
            on_delete_callback: Callback khi nhấn nút Xóa
        """
        print(f"👁️ Xem chi tiết: {patient_data[2]} (ID: {patient_data[1]})")
        
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Chi tiết bệnh nhân")
        popup.geometry("1000x700")
        popup.resizable(False, False)
        
        # Đặt màu nền xanh cho popup
        popup.configure(fg_color="#F7F7F5")  # Màu xanh nhạt
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        popup.after(100, lambda: popup.attributes('-topmost', False))
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (1000 // 2)
        y = (popup.winfo_screenheight() // 2) - (700 // 2)
        popup.geometry(f"1000x700+{x}+{y}")

        # Main container với nền trắng, bo góc tròn
        main_container = ctk.CTkFrame(popup, fg_color="#F7F7F5" )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cấu hình grid - 3 rows
        main_container.grid_rowconfigure(0, weight=0)  # Row 0: Tiêu đề
        main_container.grid_rowconfigure(1, weight=1)  # Row 1: Nội dung chính (Avatar + Fields)
        main_container.grid_rowconfigure(2, weight=0)  # Row 2: Buttons
        main_container.grid_columnconfigure(0, weight=1)
        
        # ==================== ROW 0: TIÊU ĐỀ ====================
        title_frame = ctk.CTkFrame(main_container, fg_color="#66B7FF", corner_radius=8 , border_width=2, border_color="black")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="📋 THÔNG TIN BỆNH NHÂN",
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
            corner_radius=10, 
            width=200, 
            height=283,
            border_width=3,
            border_color="#FE5858"
        )
        avatar_frame.pack()
        avatar_frame.pack_propagate(False)
        
        # Label hiển thị ảnh (sẽ được update khi tải ảnh)
        self.avatar_image_label = ctk.CTkLabel(
            avatar_frame,
            text="👤\nChưa có ảnh",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#757575"
        )
        self.avatar_image_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Lưu reference ảnh để tránh garbage collection
        self.avatar_photo = [None]
        
        # Text "Ảnh đại diện" dưới avatar
        avatar_text = ctk.CTkLabel(
            avatar_container,
            text="Ảnh đại diện",
            font=ctk.CTkFont(size=12),
            text_color="#757575",
        )
        avatar_text.pack(pady=(5, 10))
        
        # Nút tải ảnh
        def upload_avatar():
            """Mở hộp thoại chọn ảnh từ máy tính"""
            def on_success(image, file_path):
                """Callback khi tải ảnh thành công"""
                # Chuyển đổi sang CTkImage
                ctk_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(image.width, image.height)
                )
                
                # Cập nhật label với ảnh mới
                self.avatar_image_label.configure(image=ctk_image, text="")
                self.avatar_photo[0] = ctk_image  # Lưu reference
            
            def on_error(error_msg):
                """Callback khi có lỗi"""
                self.show_warning_popup(error_msg)
            
            # Gọi controller xử lý
            self.detail_controller.upload_avatar(
                self.avatar_image_label,
                on_success_callback=on_success,
                on_error_callback=on_error
            )
        
        upload_btn = ctk.CTkButton(
            avatar_container,
            text="📤 Tải ảnh lên",
            width=200,
            height=35,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#2196F3",
            hover_color="#45a049",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=upload_avatar
        )
        upload_btn.pack()
        
        # --- COLUMN 1: Scrollable Frame chứa các Input Fields ---
        scrollable_frame = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="transparent",
            scrollbar_button_color="#66B7FF",
            scrollbar_button_hover_color="#45a049"
        )
        scrollable_frame.grid(row=0, column=1, sticky="nsew")
        
        # Tạo dictionary lưu các entry fields
        self.entry_fields = {}
        
        # Danh sách 15 fields theo yêu cầu
        info_fields = [
            ("ID bệnh nhân:", patient_data[1] if len(patient_data) > 1 else ""),
            ("Họ và tên:", patient_data[2] if len(patient_data) > 2 else ""),
            ("Ngày sinh:", patient_data[3] if len(patient_data) > 3 else ""),
            ("Giới tính:", patient_data[4] if len(patient_data) > 4 else ""),
            ("Số điện thoại:", patient_data[5] if len(patient_data) > 5 else ""),
            ("Email:", patient_data[6] if len(patient_data) > 6 else ""),
            ("Địa chỉ:", patient_data[7] if len(patient_data) > 7 else ""),
            ("Chức vụ:", patient_data[8] if len(patient_data) > 8 else ""),
            ("Ngày bắt đầu làm việc:", patient_data[9] if len(patient_data) > 9 else ""),
            ("Cân nặng (kg):", patient_data[10] if len(patient_data) > 10 else ""),
            ("Tiểu sử bệnh lý:", patient_data[11] if len(patient_data) > 11 else ""),
            ("Tên người thân:", patient_data[12] if len(patient_data) > 12 else ""),
            ("Số điện thoại người thân:", patient_data[13] if len(patient_data) > 13 else ""),
            ("Quan hệ người thân:", patient_data[14] if len(patient_data) > 14 else ""),
            ("Ghi chú:", patient_data[15] if len(patient_data) > 15 else ""),
        ]
        
        # Tạo 15 input fields trong scrollable frame
        for i, (label_text, value) in enumerate(info_fields):
            # Frame cho mỗi field
            field_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=8, padx=5)
            
            # Label
            label = ctk.CTkLabel(
                field_frame,
                text=label_text,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="black",
                anchor="w",
                width=200
            )
            label.pack(side="left", padx=(0, 15))
            
            # Entry (read-only ban đầu)
            # Sử dụng CTkTextbox cho các trường dài (Tiểu sử bệnh lý, Ghi chú)
            if label_text in ["Tiểu sử bệnh lý:", "Ghi chú:"]:
                entry = ctk.CTkTextbox(
                    field_frame,
                    height=80,
                    fg_color="white",       
                    text_color="black",
                    corner_radius=10,
                    border_width=2,
                    border_color="black",  
                    font=ctk.CTkFont(size=13),
                    wrap="word"
                )
                entry.insert("1.0", str(value))
                entry.configure(state="disabled")
                entry.pack(side="left", fill="x", expand=True)
            else:
                entry = ctk.CTkEntry(
                    field_frame,
                    height=35,
                    fg_color="white",
                    text_color="black",
                    corner_radius=10,
                    border_width=2,
                    border_color="black", 
                    font=ctk.CTkFont(size=13)
                )
                entry.insert(0, str(value))
                entry.configure(state="readonly")
                entry.pack(side="left", fill="x", expand=True)
            
            # Lưu entry vào dictionary để có thể chỉnh sửa sau
            field_key = label_text.replace(":", "").replace(" ", "_").lower()
            self.entry_fields[field_key] = entry
        
        # ==================== ROW 2: BUTTONS (3 NÚT) ====================
        button_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew")
        
        # Căn giữa các button
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_frame.grid_columnconfigure(3, weight=0)
        button_frame.grid_columnconfigure(4, weight=1)
        
        # Biến theo dõi chế độ chỉnh sửa - không cần nữa vì đã có trong controller
        
        def toggle_edit_or_save():
            """Chuyển đổi giữa chế độ chỉnh sửa và lưu"""
            # Sử dụng controller để toggle edit mode
            is_now_editing = self.detail_controller.toggle_edit_mode(
                self.entry_fields,
                edit_save_btn
            )
            
            # Nếu vừa chuyển từ edit sang view (đã lưu)
            if not is_now_editing:
                # Lưu dữ liệu
                def on_save_success(updated_data):
                    print(f"✅ Lưu thành công: {updated_data.get('họ_và_tên', 'N/A')}")
                
                self.detail_controller.save_patient_data(
                    self.entry_fields,
                    patient_id=patient_data[1] if len(patient_data) > 1 else None,
                    on_success_callback=on_save_success
                )
        
        def export_to_pdf():
            """Xuất thông tin ra file PDF"""
            def on_error(error_msg):
                """Callback khi có lỗi"""
                self.show_warning_popup(error_msg)
            
            # Gọi controller xử lý
            self.detail_controller.export_to_pdf(
                patient_data,
                entry_fields=self.entry_fields,
                on_error_callback=on_error
            )
        
        # Nút Quay lại
        back_btn = ctk.CTkButton(
            button_frame,
            text="◀ Quay lại",
            width=180,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#66B7FF",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=popup.destroy
        )
        back_btn.grid(row=0, column=1, padx=10)
        
        # Nút Chỉnh sửa/Lưu (2 trong 1)
        edit_save_btn = ctk.CTkButton(
            button_frame,
            text="✏️ Chỉnh sửa",
            width=180,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#FFA726",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=toggle_edit_or_save
        )
        edit_save_btn.grid(row=0, column=2, padx=10)
        
        # Nút Xuất PDF
        pdf_btn = ctk.CTkButton(
            button_frame,
            text="📄 Xuất PDF",
            width=180,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#E91E63",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=export_to_pdf
        )
        pdf_btn.grid(row=0, column=3, padx=10)

