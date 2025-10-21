import customtkinter as ctk
from matplotlib.figure import Figure
from PIL import Image , ImageTk , ImageDraw, ImageOps
from assets.Assets_Management import AssetManager

class AI_UI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent" )
        self.pack(fill="both", expand=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=8)

        # Frame 1:Bảng thông tin bệnh nhân
        self.Frame_Patient_Info = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=10)
        self.Frame_Patient_Info.grid(row=0, column=0, sticky="nsew", padx=(8,0), pady=10)
        self.Frame_Patient_Info.grid_rowconfigure(0, weight=1)
        self.Frame_Patient_Info.grid_rowconfigure(1, weight=1)
        self.Frame_Patient_Info.grid_rowconfigure(2, weight=1)
        self.Frame_Patient_Info.grid_columnconfigure(0, weight=1)

         # ========== Label tiêu đề ==========
        title = ctk.CTkLabel(self.Frame_Patient_Info, text="THÔNG TIN BỆNH NHÂN",text_color="black", font=ctk.CTkFont(size=16, weight="bold" , family ="Roboto"))
        title.grid(row=0, column=0, pady=(5,0), sticky="n")

        self.Searching_info_patient(self.Frame_Patient_Info)
        self.Display_info_patient(self.Frame_Patient_Info)

        # Frame 2:Bảng phân tích AI
        self.Frame_AI_Analysis = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=10)
        self.Frame_AI_Analysis.grid(row=0, column=1, sticky="nsew", padx=(5,8), pady=10)
        
        self.AI_Analysis_Form(self.Frame_AI_Analysis)

    # Frame 1:Bảng thông tin bệnh nhân
    # ========== LAYER SEARCHING INFO PATIENT ==========
    def Searching_info_patient(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="white" )
        frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0,5))
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=9)
        frame.grid_columnconfigure(1, weight=1)

        # ========== Label tiêu đề ==========
        title = ctk.CTkLabel(frame, text="Mã bệnh nhân", text_color= "black" , font=ctk.CTkFont(size=10, weight="bold") , anchor="w", justify="left"  )
        title.grid(row=0, column=0, padx=(10,0), pady=(5,0), sticky="ws", columnspan=2)

        # ========== Entry tìm kiếm ==========
        self.entry_search = ctk.CTkEntry(frame, placeholder_text="Nhập mã bệnh nhân", font=ctk.CTkFont(size=10), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=35)
        self.entry_search.grid(row=1, column=0, padx=(5,0), pady=(0,5), sticky="we")

        # ========== Nút tìm kiếm ==========
        self.button_search = ctk.CTkButton(frame, text="Tìm kiếm", font=ctk.CTkFont(size=14, weight="bold"), width=100, height=35 , hover_color="#45a049", fg_color="#66B7FF", border_width=2, border_color="black", corner_radius=10)
        self.button_search.grid(row=1, column=1, padx=(3,5), pady=(0,5), sticky="we")

    # ========== HIỂN THỊ THÔNG TIN BỆNH NHÂN ==========
    def Display_info_patient(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="white", border_width=2, border_color="black", corner_radius=10 )
        frame.grid(row=2, column=0, columnspan=1, sticky="nsew", padx=10, pady=(0,5))

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
        title = ctk.CTkLabel(frame, text="THÔNG TIN BỆNH NHÂN",text_color="black", font=ctk.CTkFont(size=14, weight="bold") , anchor="w", justify="left"   )
        title.grid(row=0, column=0, columnspan=2, padx=5, pady=(5,0) , sticky="n")

        # ========== Label và Entry thông tin bệnh nhân ==========
        
        # Mã bệnh nhân
        label_id = ctk.CTkLabel(frame, text="Mã bệnh nhân: ",text_color="black", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_id.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        entry_id = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_id.grid(row=1, column=1, padx=(0,10), pady=5, sticky="ew")

        # Họ và tên
        label_name = ctk.CTkLabel(frame, text="Họ và tên: ",text_color="black", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_name.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        entry_name = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_name.grid(row=2, column=1, padx=(0,10), pady=5, sticky="ew")

        # Tuổi
        label_age = ctk.CTkLabel(frame, text="Tuổi: ",text_color="black", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_age.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        entry_age = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_age.grid(row=3, column=1, padx=(0,10), pady=5, sticky="ew")

        # Giới tính
        label_gender = ctk.CTkLabel(frame, text="Giới tính: ",text_color="black", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_gender.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        entry_gender = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_gender.grid(row=4, column=1, padx=(0,10), pady=5, sticky="ew")

        # Lý do vào viện
        label_reason = ctk.CTkLabel(frame, text="Lý do vào viện: ",text_color="black", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_reason.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        
        entry_reason = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_reason.grid(row=5, column=1, padx=(0,10), pady=5, sticky="ew")

        # Ngày nhập viện
        label_admission_date = ctk.CTkLabel(frame, text="Ngày nhập viện: ",text_color="black", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_admission_date.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        
        entry_admission_date = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_admission_date.grid(row=6, column=1, padx=(0,10), pady=5, sticky="ew")

        # Bác sĩ điều trị
        label_doctor = ctk.CTkLabel(frame, text="Bác sĩ điều trị: ",text_color="black", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_doctor.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        
        entry_doctor = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_doctor.grid(row=7, column=1, padx=(0,10), pady=5, sticky="ew")

        # ========== Frame chứa 3 nút ==========
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=8, column=0, columnspan=2, padx=5, pady=(5,10), sticky="ew")
        # Cột trống bên trái để đẩy 3 nút ra giữa
        button_frame.grid_columnconfigure(0, weight=1)
        # 3 nút không dùng weight (giữ nguyên kích thước)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_frame.grid_columnconfigure(3, weight=0)
        # Cột trống bên phải để cân bằng
        button_frame.grid_columnconfigure(4, weight=1)

        # ========== 3 Nút: Xem, Sửa, Xóa (căn giữa) ==========
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
        self.button_detail.grid(row=0, column=1, padx=(0,3), pady=0)

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
        self.button_delete.grid(row=0, column=3, padx=(3,0), pady=0)

    # Frame 2:Bảng phân tích AI
    # ========== FORM PHÂN TÍCH AI ==========
    def AI_Analysis_Form(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="white")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cấu hình grid
        frame.grid_rowconfigure(0, weight=2)  # Row 0 - View hiển thị kết quả (chiếm nhiều không gian hơn)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_rowconfigure(7, weight=1)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        
        # ========== ROW 0: View hiển thị kết quả ==========
        result_view = ctk.CTkFrame(frame, fg_color="#F7F7F5", border_width=2, border_color="black", corner_radius=10)
        result_view.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        # ========== ROW 1: 4 columns ==========
        label_row1_col0 = ctk.CTkLabel(frame, text="Nhãn 1.0:", text_color="black", font=ctk.CTkFont(size=12))
        label_row1_col0.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        entry_row1_col1 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row1_col1.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        label_row1_col2 = ctk.CTkLabel(frame, text="Nhãn 1.2:", text_color="black", font=ctk.CTkFont(size=12))
        label_row1_col2.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        entry_row1_col3 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row1_col3.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        # ========== ROW 2: 4 columns ==========
        label_row2_col0 = ctk.CTkLabel(frame, text="Nhãn 2.0:", text_color="black", font=ctk.CTkFont(size=12))
        label_row2_col0.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        entry_row2_col1 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row2_col1.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        label_row2_col2 = ctk.CTkLabel(frame, text="Nhãn 2.2:", text_color="black", font=ctk.CTkFont(size=12))
        label_row2_col2.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        entry_row2_col3 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row2_col3.grid(row=2, column=3, padx=5, pady=5, sticky="ew")
        
        # ========== ROW 3: 4 columns ==========
        label_row3_col0 = ctk.CTkLabel(frame, text="Nhãn 3.0:", text_color="black", font=ctk.CTkFont(size=12))
        label_row3_col0.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        entry_row3_col1 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row3_col1.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        label_row3_col2 = ctk.CTkLabel(frame, text="Nhãn 3.2:", text_color="black", font=ctk.CTkFont(size=12))
        label_row3_col2.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        
        entry_row3_col3 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row3_col3.grid(row=3, column=3, padx=5, pady=5, sticky="ew")
        
        # ========== ROW 4: 4 columns ==========
        label_row4_col0 = ctk.CTkLabel(frame, text="Nhãn 4.0:", text_color="black", font=ctk.CTkFont(size=12))
        label_row4_col0.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        entry_row4_col1 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row4_col1.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        label_row4_col2 = ctk.CTkLabel(frame, text="Nhãn 4.2:", text_color="black", font=ctk.CTkFont(size=12))
        label_row4_col2.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        
        entry_row4_col3 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row4_col3.grid(row=4, column=3, padx=5, pady=5, sticky="ew")
        
        # ========== ROW 5: 4 columns ==========
        label_row5_col0 = ctk.CTkLabel(frame, text="Nhãn 5.0:", text_color="black", font=ctk.CTkFont(size=12))
        label_row5_col0.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        
        entry_row5_col1 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row5_col1.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        
        label_row5_col2 = ctk.CTkLabel(frame, text="Nhãn 5.2:", text_color="black", font=ctk.CTkFont(size=12))
        label_row5_col2.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        
        entry_row5_col3 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row5_col3.grid(row=5, column=3, padx=5, pady=5, sticky="ew")
        
        # ========== ROW 6: 4 columns ==========
        label_row6_col0 = ctk.CTkLabel(frame, text="Nhãn 6.0:", text_color="black", font=ctk.CTkFont(size=12))
        label_row6_col0.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        
        entry_row6_col1 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row6_col1.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        
        label_row6_col2 = ctk.CTkLabel(frame, text="Nhãn 6.2:", text_color="black", font=ctk.CTkFont(size=12))
        label_row6_col2.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        
        entry_row6_col3 = ctk.CTkEntry(frame, font=ctk.CTkFont(size=12), fg_color="#F7F7F5", border_color="black", border_width=2, corner_radius=10, height=26)
        entry_row6_col3.grid(row=6, column=3, padx=5, pady=5, sticky="ew")
        
        # ========== ROW 7: 2 nút (Chạy chương trình và Xóa) ==========
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky="ews")
        
        # Cấu hình button_frame để căn giữa 2 nút
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_frame.grid_columnconfigure(3, weight=1)
        
        # Nút chạy chương trình
        self.button_run = ctk.CTkButton(
            button_frame,
            text="Chạy chương trình",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=150,
            height=35,
            fg_color="#66B7FF",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            corner_radius=10
        )
        self.button_run.grid(row=0, column=1, padx=5, pady=0)
        
        # Nút xóa
        self.button_clear = ctk.CTkButton(
            button_frame,
            text="Xóa",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=100,
            height=35,
            fg_color="#ED5C5C",
            hover_color="#c44a4a",
            border_width=2,
            border_color="black",
            corner_radius=10
        )
        self.button_clear.grid(row=0, column=2, padx=5, pady=0)
