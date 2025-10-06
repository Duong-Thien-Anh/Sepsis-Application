import customtkinter as ctk
from matplotlib.figure import Figure
from PIL import Image , ImageTk , ImageDraw, ImageOps
from assets.Assets_Management import AssetManager

class AI_UI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent" , corner_radius=15 , border_color="#000000", border_width=2)
        self.pack(fill="both", expand=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Frame 1:Bảng thông tin bệnh nhân
        self.Frame_Patient_Info = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=10)
        self.Frame_Patient_Info.grid(row=0, column=0, sticky="nsew", padx=(10,0), pady=10)
        self.Frame_Patient_Info.grid_rowconfigure(0, weight=1)
        self.Frame_Patient_Info.grid_rowconfigure(1, weight=1)
        self.Frame_Patient_Info.grid_rowconfigure(2, weight=1)
        self.Frame_Patient_Info.grid_columnconfigure(0, weight=1)

         # ========== Label tiêu đề ==========
        title = ctk.CTkLabel(self.Frame_Patient_Info, text="THÔNG TIN BỆNH NHÂN", font=ctk.CTkFont(size=16, weight="bold" , family ="Roboto"))
        title.grid(row=0, column=0, pady=5, sticky="n")

        self.Searching_info_patient(self.Frame_Patient_Info)
        self.Display_info_patient(self.Frame_Patient_Info)

        # Frame 2:Bảng phân tích AI
        self.Frame_AI_Analysis = ctk.CTkFrame(self, fg_color="red", border_width=2, border_color="black", corner_radius=10)
        self.Frame_AI_Analysis.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=10)

        


    # ========== LAYER SEARCHING INFO PATIENT ==========
    def Searching_info_patient(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="white", border_width=2, border_color="black", corner_radius=10 )
        frame.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=(0,10))
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=8)
        frame.grid_columnconfigure(1, weight=2)

        # ========== Label tiêu đề ==========
        title = ctk.CTkLabel(frame, text="TÌM KIẾM MÃ BỆNH NHÂN", font=ctk.CTkFont(size=14, weight="bold") , anchor="w", justify="left" , wraplength=100  )
        title.grid(row=0, column=0, padx=5, pady=10)

        # ========== Entry tìm kiếm ==========
        self.entry_search = ctk.CTkEntry(frame, placeholder_text="Nhập mã bệnh nhân", font=ctk.CTkFont(size=14), width=200)
        self.entry_search.grid(row=1, column=0, padx=0, pady=(0,5), sticky="ns")

        # ========== Nút tìm kiếm ==========
        self.button_search = ctk.CTkButton(frame, text="Tìm kiếm", font=ctk.CTkFont(size=14, weight="bold"), width=100)
        self.button_search.grid(row=1, column=1, padx=10, pady=(0,5), sticky="ns")

    # ========== HIỂN THỊ THÔNG TIN BỆNH NHÂN ==========
    def Display_info_patient(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="white", border_width=2, border_color="black", corner_radius=10 )
        frame.grid(row=2, column=0, columnspan=1, sticky="nsew", padx=10, pady=(0,10))
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # ========== Label tiêu đề ==========
        title = ctk.CTkLabel(frame, text="THÔNG TIN BỆNH NHÂN", font=ctk.CTkFont(size=14, weight="bold") , anchor="w", justify="left" , wraplength=100  )
        title.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        # ========== Label thông tin bệnh nhân ==========
        label_id = ctk.CTkLabel(frame, text="Mã bệnh nhân: ", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_id.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        label_name = ctk.CTkLabel(frame, text="Họ và tên: ", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_name.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        label_age = ctk.CTkLabel(frame, text="Tuổi: ", font=ctk.CTkFont(size=12) , anchor="w", justify="left" , wraplength=100  )
        label_age.grid(row=3, column=0, padx=5, pady=5, sticky="w")
