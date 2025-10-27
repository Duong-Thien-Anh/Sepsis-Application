import customtkinter as ctk
from controllers.Patient_Controller import PatientController

class PatientDetailPopups:
    """Class quản lý tất cả các popup UI liên quan đến bệnh nhân."""
    
    def __init__(self, parent, controller):
        """
        Args:
            parent: Component cha (Patient_UI)
            controller: PatientController instance
        """
        self.parent = parent
        self.controller = controller
    
    # ==================== DETAIL POPUP ====================
    
    def show_patient_detail(self, patient_data, on_edit_callback, on_delete_callback):
        """Hiển thị popup chi tiết bệnh nhân.
        
        Args:
            patient_data (tuple): (STT, ID, Họ tên, Ngày sinh, Giới tính, SDT, Email)
            on_edit_callback: Callback khi nhấn nút Sửa
            on_delete_callback: Callback khi nhấn nút Xóa
        """
        print(f"👁️ Xem chi tiết: {patient_data[2]} (ID: {patient_data[1]})")
        
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Chi tiết bệnh nhân")
        popup.geometry("550x650")
        popup.resizable(False, False)
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        popup.after(100, lambda: popup.attributes('-topmost', False))
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (550 // 2)
        y = (popup.winfo_screenheight() // 2) - (650 // 2)
        popup.geometry(f"550x650+{x}+{y}")
        
        # Header
        header = ctk.CTkFrame(popup, fg_color="#66B7FF", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="📋 THÔNG TIN CHI TIẾT BỆNH NHÂN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title.pack(pady=15)
        
        # Content
        content = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Thông tin chi tiết
        info_fields = [
            ("STT:", patient_data[0]),
            ("Mã bệnh nhân:", patient_data[1]),
            ("Họ và tên:", patient_data[2]),
            ("Ngày sinh:", patient_data[3]),
            ("Giới tính:", patient_data[4]),
            ("Số điện thoại:", patient_data[5]),
            ("Email:", patient_data[6]),
        ]
        
        for i, (label_text, value) in enumerate(info_fields):
            # Frame cho mỗi field
            field_frame = ctk.CTkFrame(content, fg_color="#f0f0f0", corner_radius=8)
            field_frame.pack(fill="x", pady=8)
            
            # Label
            label = ctk.CTkLabel(
                field_frame,
                text=label_text,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                width=150
            )
            label.pack(side="left", padx=15, pady=12)
            
            # Value
            value_label = ctk.CTkLabel(
                field_frame,
                text=value,
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            value_label.pack(side="left", padx=10, pady=12)
        
        # Footer buttons
        footer = ctk.CTkFrame(popup, fg_color="transparent")
        footer.pack(fill="x", padx=30, pady=(0, 20))
        
        # Nút Sửa
        edit_btn = ctk.CTkButton(
            footer,
            text="✏️ Chỉnh sửa",
            width=150,
            height=42,
            corner_radius=8,
            fg_color="#FFA726",
            hover_color="#FB8C00",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: [popup.destroy(), on_edit_callback(patient_data)]
        )
        edit_btn.pack(side="left", padx=5)
        
        # Nút Xóa
        delete_btn = ctk.CTkButton(
            footer,
            text="🗑️ Xóa",
            width=150,
            height=42,
            corner_radius=8,
            fg_color="#F44336",
            hover_color="#da190b",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: [popup.destroy(), on_delete_callback(patient_data)]
        )
        delete_btn.pack(side="left", padx=5)
        
        # Nút Đóng
        close_btn = ctk.CTkButton(
            footer,
            text="❌ Đóng",
            width=150,
            height=42,
            corner_radius=8,
            fg_color="#66B7FF",
            hover_color="#5aa3e0",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=popup.destroy
        )
        close_btn.pack(side="left", padx=5)
    
    # ==================== ADD FORM ====================
    
    def show_add_patient_form(self, on_save_callback):
        """Hiển thị form thêm bệnh nhân mới.
        
        Args:
            on_save_callback: Callback(fields_dict, popup) khi nhấn nút Lưu
        """
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Thêm bệnh nhân mới")
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
        header = ctk.CTkFrame(popup, fg_color="#4CAF50", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="➕ THÊM BỆNH NHÂN MỚI",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title.pack(pady=15)
        
        # Content
        content = ctk.CTkFrame(popup, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Fields
        fields = {}
        
        # Họ và tên
        ctk.CTkLabel(content, text="Họ và tên:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['full_name'] = ctk.CTkEntry(content, height=40, font=ctk.CTkFont(size=13))
        fields['full_name'].pack(fill="x", pady=(0,10))
        
        # Ngày sinh
        ctk.CTkLabel(content, text="Ngày sinh (DD/MM/YYYY):", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['birth_date'] = ctk.CTkEntry(content, height=40, font=ctk.CTkFont(size=13), placeholder_text="01/01/1990")
        fields['birth_date'].pack(fill="x", pady=(0,10))
        
        # Giới tính
        ctk.CTkLabel(content, text="Giới tính:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['gender'] = ctk.CTkOptionMenu(content, values=["Nam", "Nữ"], height=40, font=ctk.CTkFont(size=13))
        fields['gender'].set("Nam")
        fields['gender'].pack(fill="x", pady=(0,10))
        
        # Số điện thoại
        ctk.CTkLabel(content, text="Số điện thoại:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['phone'] = ctk.CTkEntry(content, height=40, font=ctk.CTkFont(size=13), placeholder_text="0901234567")
        fields['phone'].pack(fill="x", pady=(0,10))
        
        # Email
        ctk.CTkLabel(content, text="Email:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10,5))
        fields['email'] = ctk.CTkEntry(content, height=40, font=ctk.CTkFont(size=13), placeholder_text="example@email.com")
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
            corner_radius=8,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: on_save_callback(fields, popup)
        )
        save_btn.pack(side="left", padx=5)
        
        # Nút Hủy
        cancel_btn = ctk.CTkButton(
            footer,
            text="❌ Hủy",
            width=220,
            height=42,
            corner_radius=8,
            fg_color="#F44336",
            hover_color="#da190b",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=popup.destroy
        )
        cancel_btn.pack(side="left", padx=5)
    
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
            corner_radius=8,
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
            corner_radius=8,
            fg_color="#F44336",
            hover_color="#da190b",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=popup.destroy
        )
        cancel_btn.pack(side="left", padx=5)
    
    # ==================== CONFIRMATION POPUPS ====================
    
    def show_confirm_delete_popup(self, patient_name, on_confirm_callback):
        """Hiển thị popup xác nhận xóa bệnh nhân.
        
        Args:
            patient_name (str): Tên bệnh nhân
            on_confirm_callback: Callback(popup) khi nhấn Yes
        """
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Xác nhận xóa")
        popup.geometry("400x180")
        popup.resizable(False, False)
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (400 // 2)
        y = (popup.winfo_screenheight() // 2) - (180 // 2)
        popup.geometry(f"400x180+{x}+{y}")
        
        # Nội dung popup
        message = f"Bạn có chắc muốn xóa bệnh nhân\n'{patient_name}' không?"
        label = ctk.CTkLabel(
            popup,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        label.pack(pady=30)
        
        # Frame chứa 2 nút Yes/No
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=10)
        
        # Nút Yes
        yes_button = ctk.CTkButton(
            button_frame,
            text="Yes",
            width=100,
            height=35,
            fg_color="#F44336",
            hover_color="#da190b",
            command=lambda: on_confirm_callback(popup)
        )
        yes_button.pack(side="left", padx=10)
        
        # Nút No
        no_button = ctk.CTkButton(
            button_frame,
            text="No",
            width=100,
            height=35,
            fg_color="#66B7FF",
            hover_color="#45a049",
            command=popup.destroy
        )
        no_button.pack(side="left", padx=10)
    
    # ==================== WARNING POPUP ====================
    
    def show_warning_popup(self, message):
        """Hiển thị popup cảnh báo.
        
        Args:
            message (str): Nội dung cảnh báo
        """
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Cảnh báo")
        popup.geometry("300x150")
        popup.resizable(False, False)
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (300 // 2)
        y = (popup.winfo_screenheight() // 2) - (150 // 2)
        popup.geometry(f"300x150+{x}+{y}")
        
        # Nội dung popup
        label = ctk.CTkLabel(
            popup,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=250
        )
        label.pack(pady=30)
        
        # Nút OK
        ok_button = ctk.CTkButton(
            popup,
            text="OK",
            width=100,
            height=35,
            fg_color="#66B7FF",
            hover_color="#45a049",
            command=popup.destroy
        )
        ok_button.pack(pady=10)
