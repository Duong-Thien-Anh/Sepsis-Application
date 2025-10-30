import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from assets.Assets_Management import AssetManager

class RecallAppointment_UI(ctk.CTkFrame):
    """Giao diện quản lý lịch tái khám và gửi thông báo."""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=8)

        # Frame 1: Bảng thông tin bệnh nhân (bên trái)
        self.Frame_Patient_Info = ctk.CTkFrame(
            self, 
            fg_color="white", 
            border_width=2, 
            border_color="black", 
            corner_radius=10
        )
        self.Frame_Patient_Info.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=10)
        self.Frame_Patient_Info.grid_rowconfigure(0, weight=1)
        self.Frame_Patient_Info.grid_rowconfigure(1, weight=1)
        self.Frame_Patient_Info.grid_rowconfigure(2, weight=1)
        self.Frame_Patient_Info.grid_columnconfigure(0, weight=1)

        # ========== Label tiêu đề ==========
        title = ctk.CTkLabel(
            self.Frame_Patient_Info, 
            text="THÔNG TIN BỆNH NHÂN",
            text_color="black", 
            font=ctk.CTkFont(size=16, weight="bold", family="Roboto")
        )
        title.grid(row=0, column=0, pady=(5, 0), sticky="n")

        self.Searching_info_patient(self.Frame_Patient_Info)
        self.Display_info_patient(self.Frame_Patient_Info)

        # Frame 2: Form gửi mail tái khám (bên phải)
        self.Frame_Recall_Mail = ctk.CTkFrame(
            self, 
            fg_color="white", 
            border_width=2, 
            border_color="black", 
            corner_radius=10
        )
        self.Frame_Recall_Mail.grid(row=0, column=1, sticky="nsew", padx=(5, 8), pady=10)
        
        self.Recall_Mail_Form(self.Frame_Recall_Mail)

    # ==================== FRAME 1: THÔNG TIN BỆNH NHÂN ====================
    
    def Searching_info_patient(self, parent):
        """Form tìm kiếm bệnh nhân."""
        frame = ctk.CTkFrame(parent, fg_color="white")
        frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=9)
        frame.grid_columnconfigure(1, weight=1)

        # ========== Label tiêu đề ==========
        title = ctk.CTkLabel(
            frame, 
            text="Mã bệnh nhân", 
            text_color="black", 
            font=ctk.CTkFont(size=10, weight="bold"), 
            anchor="w", 
            justify="left"
        )
        title.grid(row=0, column=0, padx=(10, 0), pady=(5, 0), sticky="ws", columnspan=2)

        # ========== Entry tìm kiếm ==========
        self.entry_search = ctk.CTkEntry(
            frame, 
            placeholder_text="Nhập mã bệnh nhân", 
            font=ctk.CTkFont(size=10), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=35
        )
        self.entry_search.grid(row=1, column=0, padx=(5, 0), pady=(0, 5), sticky="we")

        # ========== Nút tìm kiếm ==========
        self.button_search = ctk.CTkButton(
            frame, 
            text="Tìm kiếm", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            width=100, 
            height=35, 
            hover_color="#45a049", 
            fg_color="#66B7FF", 
            border_width=2, 
            border_color="black", 
            corner_radius=10
        )
        self.button_search.grid(row=1, column=1, padx=(3, 5), pady=(0, 5), sticky="we")

    def Display_info_patient(self, parent):
        """Hiển thị thông tin bệnh nhân."""
        frame = ctk.CTkFrame(
            parent, 
            fg_color="white", 
            border_width=2, 
            border_color="black", 
            corner_radius=10
        )
        frame.grid(row=2, column=0, columnspan=1, sticky="nsew", padx=10, pady=(0, 5))

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_rowconfigure(7, weight=1)
        frame.grid_rowconfigure(8, weight=1)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # ========== Label tiêu đề ==========
        title = ctk.CTkLabel(
            frame, 
            text="THÔNG TIN BỆNH NHÂN",
            text_color="black", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            anchor="w", 
            justify="left"
        )
        title.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="n")

        # ========== Label và Entry thông tin bệnh nhân ==========
        
        # Mã bệnh nhân
        label_id = ctk.CTkLabel(
            frame, 
            text="Mã bệnh nhân: ",
            text_color="black", 
            font=ctk.CTkFont(size=12), 
            anchor="w", 
            justify="left", 
            wraplength=100
        )
        label_id.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_patient_id = ctk.CTkEntry(
            frame, 
            font=ctk.CTkFont(size=12), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=26
        )
        self.entry_patient_id.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Họ và tên
        label_name = ctk.CTkLabel(
            frame, 
            text="Họ và tên: ",
            text_color="black", 
            font=ctk.CTkFont(size=12), 
            anchor="w", 
            justify="left", 
            wraplength=100
        )
        label_name.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_patient_name = ctk.CTkEntry(
            frame, 
            font=ctk.CTkFont(size=12), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=26
        )
        self.entry_patient_name.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Tuổi
        label_age = ctk.CTkLabel(
            frame, 
            text="Tuổi: ",
            text_color="black", 
            font=ctk.CTkFont(size=12), 
            anchor="w", 
            justify="left", 
            wraplength=100
        )
        label_age.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_patient_age = ctk.CTkEntry(
            frame, 
            font=ctk.CTkFont(size=12), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=26
        )
        self.entry_patient_age.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Giới tính
        label_gender = ctk.CTkLabel(
            frame, 
            text="Giới tính: ",
            text_color="black", 
            font=ctk.CTkFont(size=12), 
            anchor="w", 
            justify="left", 
            wraplength=100
        )
        label_gender.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_patient_gender = ctk.CTkEntry(
            frame, 
            font=ctk.CTkFont(size=12), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=26
        )
        self.entry_patient_gender.grid(row=4, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Lý do vào viện
        label_reason = ctk.CTkLabel(
            frame, 
            text="Lý do vào viện: ",
            text_color="black", 
            font=ctk.CTkFont(size=12), 
            anchor="w", 
            justify="left", 
            wraplength=100
        )
        label_reason.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_patient_reason = ctk.CTkEntry(
            frame, 
            font=ctk.CTkFont(size=12), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=26
        )
        self.entry_patient_reason.grid(row=5, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Ngày nhập viện
        label_admission_date = ctk.CTkLabel(
            frame, 
            text="Ngày nhập viện: ",
            text_color="black", 
            font=ctk.CTkFont(size=12), 
            anchor="w", 
            justify="left", 
            wraplength=100
        )
        label_admission_date.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_admission_date = ctk.CTkEntry(
            frame, 
            font=ctk.CTkFont(size=12), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=26
        )
        self.entry_admission_date.grid(row=6, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Bác sĩ điều trị
        label_doctor = ctk.CTkLabel(
            frame, 
            text="Bác sĩ điều trị: ",
            text_color="black", 
            font=ctk.CTkFont(size=12), 
            anchor="w", 
            justify="left", 
            wraplength=100
        )
        label_doctor.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_doctor = ctk.CTkEntry(
            frame, 
            font=ctk.CTkFont(size=12), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=26
        )
        self.entry_doctor.grid(row=7, column=1, padx=(0, 10), pady=5, sticky="ew")

        # ========== Frame chứa 3 nút ==========
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=8, column=0, columnspan=2, padx=5, pady=(5, 10), sticky="ew")
        
        # Cột trống bên trái để đẩy 3 nút ra giữa
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_frame.grid_columnconfigure(3, weight=0)
        button_frame.grid_columnconfigure(4, weight=1)

        # ========== 3 Nút: Chi tiết, Sửa, Xóa ==========
        self.button_detail = ctk.CTkButton(
            button_frame, 
            text="Chi tiết", 
            font=ctk.CTkFont(size=12, weight="bold"), 
            width=70,
            height=35,
            fg_color="#66B7FF",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            corner_radius=10
        )
        self.button_detail.grid(row=0, column=1, padx=(0, 3), pady=0)

        self.button_edit = ctk.CTkButton(
            button_frame, 
            text="Sửa", 
            font=ctk.CTkFont(size=12, weight="bold"), 
            width=70,
            height=35,
            fg_color="#F3C852",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            corner_radius=10
        )
        self.button_edit.grid(row=0, column=2, padx=3, pady=0)

        self.button_delete = ctk.CTkButton(
            button_frame, 
            text="Xóa", 
            font=ctk.CTkFont(size=12, weight="bold"), 
            width=70,
            height=35,
            fg_color="#ED5C5C",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            corner_radius=10
        )
        self.button_delete.grid(row=0, column=3, padx=(3, 0), pady=0)

    # ==================== FRAME 2: FORM GỬI MAIL TÁI KHÁM ====================
    
    def Recall_Mail_Form(self, parent):
        """Form gửi mail thông báo tái khám."""
        frame = ctk.CTkFrame(parent, fg_color="white")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cấu hình grid
        frame.grid_rowconfigure(0, weight=0)  # Tiêu đề
        frame.grid_rowconfigure(1, weight=0)  # Gửi đến
        frame.grid_rowconfigure(2, weight=0)  # Tiêu đề email
        frame.grid_rowconfigure(3, weight=0)  # Ngày hẹn
        frame.grid_rowconfigure(4, weight=1)  # Nội dung (chiếm nhiều không gian)
        frame.grid_rowconfigure(5, weight=0)  # File đính kèm
        frame.grid_rowconfigure(6, weight=0)  # Hình ảnh đính kèm
        frame.grid_rowconfigure(7, weight=0)  # Buttons
        
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        
        # ========== TIÊU ĐỀ ==========
        title = ctk.CTkLabel(
            frame, 
            text="THÔNG BÁO TÁI KHÁM",
            text_color="black", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="n")
        
        # ========== GỬI ĐẾN (Email người nhận) ==========
        label_to = ctk.CTkLabel(
            frame, 
            text="Gửi đến:",
            text_color="black", 
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label_to.grid(row=1, column=0, padx=(10, 10), pady=5, sticky="w")
        
        self.entry_to = ctk.CTkEntry(
            frame, 
            placeholder_text="Email người nhận",
            font=ctk.CTkFont(size=13), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=35
        )
        self.entry_to.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="ew")
        
        # ========== TIÊU ĐỀ EMAIL ==========
        label_subject = ctk.CTkLabel(
            frame, 
            text="Tiêu đề:",
            text_color="black", 
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label_subject.grid(row=2, column=0, padx=(10, 10), pady=5, sticky="w")
        
        self.entry_subject = ctk.CTkEntry(
            frame, 
            placeholder_text="Tiêu đề email",
            font=ctk.CTkFont(size=13), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=35
        )
        self.entry_subject.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")
        
        # ========== NGÀY HẸN TÁI KHÁM ==========
        label_date = ctk.CTkLabel(
            frame, 
            text="Ngày hẹn:",
            text_color="black", 
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label_date.grid(row=3, column=0, padx=(10, 10), pady=5, sticky="w")
        
        self.entry_date = ctk.CTkEntry(
            frame, 
            placeholder_text="DD/MM/YYYY",
            font=ctk.CTkFont(size=13), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=35
        )
        self.entry_date.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="ew")
        
        # ========== NỘI DUNG EMAIL ==========
        label_content = ctk.CTkLabel(
            frame, 
            text="Nội dung:",
            text_color="black", 
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="nw"
        )
        label_content.grid(row=4, column=0, padx=(10, 10), pady=5, sticky="nw")
        
        self.textbox_content = ctk.CTkTextbox(
            frame,
            font=ctk.CTkFont(size=13), 
            fg_color="#F7F7F5", 
            border_color="black", 
            border_width=2, 
            corner_radius=10,
            wrap="word"
        )
        self.textbox_content.grid(row=4, column=1, padx=(0, 10), pady=5, sticky="nsew")
        
        # ========== FILE ĐÍNH KÈM ==========
        label_file = ctk.CTkLabel(
            frame, 
            text="File đính kèm:",
            text_color="black", 
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label_file.grid(row=5, column=0, padx=(10, 10), pady=5, sticky="w")
        
        file_frame = ctk.CTkFrame(frame, fg_color="transparent")
        file_frame.grid(row=5, column=1, padx=(0, 10), pady=5, sticky="ew")
        file_frame.grid_columnconfigure(0, weight=1)
        file_frame.grid_columnconfigure(1, weight=0)
        
        self.entry_file = ctk.CTkEntry(
            file_frame, 
            placeholder_text="Chưa có file đính kèm",
            font=ctk.CTkFont(size=12), 
            fg_color="#E8E8E8", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=35,
            state="disabled"
        )
        self.entry_file.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.button_attach_file = ctk.CTkButton(
            file_frame, 
            text="📎 Kèm file",
            font=ctk.CTkFont(size=12, weight="bold"), 
            width=120,
            height=35,
            fg_color="#66B7FF",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            corner_radius=10,
            command=self.attach_file
        )
        self.button_attach_file.grid(row=0, column=1, sticky="e")
        
        # ========== HÌNH ẢNH ĐÍNH KÈM ==========
        label_image = ctk.CTkLabel(
            frame, 
            text="Hình ảnh:",
            text_color="black", 
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label_image.grid(row=6, column=0, padx=(10, 10), pady=5, sticky="w")
        
        image_frame = ctk.CTkFrame(frame, fg_color="transparent")
        image_frame.grid(row=6, column=1, padx=(0, 10), pady=5, sticky="ew")
        image_frame.grid_columnconfigure(0, weight=1)
        image_frame.grid_columnconfigure(1, weight=0)
        
        self.entry_image = ctk.CTkEntry(
            image_frame, 
            placeholder_text="Chưa có hình ảnh đính kèm",
            font=ctk.CTkFont(size=12), 
            fg_color="#E8E8E8", 
            border_color="black", 
            border_width=2, 
            corner_radius=10, 
            height=35,
            state="disabled"
        )
        self.entry_image.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.button_attach_image = ctk.CTkButton(
            image_frame, 
            text="🖼️ Kèm ảnh",
            font=ctk.CTkFont(size=12, weight="bold"), 
            width=120,
            height=35,
            fg_color="#66B7FF",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            corner_radius=10,
            command=self.attach_image
        )
        self.button_attach_image.grid(row=0, column=1, sticky="e")
        
        # ========== BUTTONS (Gửi và Xóa) ==========
        button_action_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_action_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=(15, 10), sticky="ew")
        
        # Cấu hình để căn giữa 2 nút
        button_action_frame.grid_columnconfigure(0, weight=1)
        button_action_frame.grid_columnconfigure(1, weight=0)
        button_action_frame.grid_columnconfigure(2, weight=0)
        button_action_frame.grid_columnconfigure(3, weight=1)
        
        # Nút Gửi
        self.button_send = ctk.CTkButton(
            button_action_frame,
            text="📧 Gửi email",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            corner_radius=10,
            command=self.send_email
        )
        self.button_send.grid(row=0, column=1, padx=5, pady=0)
        
        # Nút Xóa
        self.button_clear = ctk.CTkButton(
            button_action_frame, 
            text="🗑️ Xóa",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=120,
            height=40,
            fg_color="#ED5C5C", 
            hover_color="#da190b",
            border_width=2,
            border_color="black",
            corner_radius=10,
            command=self.clear_form
        )
        self.button_clear.grid(row=0, column=2, padx=5, pady=0)
    
    # ==================== METHODS ====================
    
    def attach_file(self):
        """Mở hộp thoại chọn file đính kèm."""
        file_path = filedialog.askopenfilename(
            title="Chọn file đính kèm",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Word files", "*.doc *.docx"),
                ("Excel files", "*.xls *.xlsx"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.entry_file.configure(state="normal")
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, file_path)
            self.entry_file.configure(state="disabled")
    
    def attach_image(self):
        """Mở hộp thoại chọn hình ảnh đính kèm."""
        image_path = filedialog.askopenfilename(
            title="Chọn hình ảnh đính kèm",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if image_path:
            self.entry_image.configure(state="normal")
            self.entry_image.delete(0, "end")
            self.entry_image.insert(0, image_path)
            self.entry_image.configure(state="disabled")
    
    def send_email(self):
        """Gửi email thông báo tái khám."""
        # Thu thập dữ liệu
        email_to = self.entry_to.get().strip()
        subject = self.entry_subject.get().strip()
        date = self.entry_date.get().strip()
        content = self.textbox_content.get("1.0", "end-1c").strip()
        file_attachment = self.entry_file.get().strip()
        image_attachment = self.entry_image.get().strip()
        
        # Validate
        if not email_to:
            self.show_warning("Vui lòng nhập email người nhận!")
            return
        
        if not subject:
            self.show_warning("Vui lòng nhập tiêu đề email!")
            return
        
        if not date:
            self.show_warning("Vui lòng nhập ngày hẹn tái khám!")
            return
        
        if not content:
            self.show_warning("Vui lòng nhập nội dung email!")
            return
        
        # TODO: Gọi API để gửi email
        # success = send_recall_email(email_to, subject, date, content, file_attachment, image_attachment)
        # if success:
        #     self.show_success("Gửi email thành công!")
        #     self.clear_form()
        # else:
        #     self.show_warning("Gửi email thất bại!")
        
        # Giả lập gửi thành công
        self.show_success("Gửi email thông báo tái khám thành công!")
        self.clear_form()
    
    def clear_form(self):
        """Xóa toàn bộ form."""
        self.entry_to.delete(0, "end")
        self.entry_subject.delete(0, "end")
        self.entry_date.delete(0, "end")
        self.textbox_content.delete("1.0", "end")
        
        self.entry_file.configure(state="normal")
        self.entry_file.delete(0, "end")
        self.entry_file.insert(0, "Chưa có file đính kèm")
        self.entry_file.configure(state="disabled")
        
        self.entry_image.configure(state="normal")
        self.entry_image.delete(0, "end")
        self.entry_image.insert(0, "Chưa có hình ảnh đính kèm")
        self.entry_image.configure(state="disabled")
    
    def show_warning(self, message):
        """Hiển thị popup cảnh báo."""
        popup = ctk.CTkToplevel(self)
        popup.title("Cảnh báo")
        popup.geometry("300x150")
        popup.resizable(False, False)
        
        popup.lift()
        popup.attributes('-topmost', True)
        
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (300 // 2)
        y = (popup.winfo_screenheight() // 2) - (150 // 2)
        popup.geometry(f"300x150+{x}+{y}")
        
        label = ctk.CTkLabel(
            popup,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=250
        )
        label.pack(pady=30)
        
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
    
    def show_success(self, message):
        """Hiển thị popup thành công."""
        popup = ctk.CTkToplevel(self)
        popup.title("Thành công")
        popup.geometry("300x150")
        popup.resizable(False, False)
        
        popup.lift()
        popup.attributes('-topmost', True)
        
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (300 // 2)
        y = (popup.winfo_screenheight() // 2) - (150 // 2)
        popup.geometry(f"300x150+{x}+{y}")
        
        label = ctk.CTkLabel(
            popup,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=250,
            text_color="#4CAF50"
        )
        label.pack(pady=30)
        
        ok_button = ctk.CTkButton(
            popup,
            text="OK",
            width=100,
            height=35,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=popup.destroy
        )
        ok_button.pack(pady=10)
