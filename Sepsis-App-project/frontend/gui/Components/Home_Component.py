import customtkinter as ctk
from matplotlib.figure import Figure
from PIL import Image , ImageTk , ImageDraw, ImageOps
import requests
from controllers.Home_Controller import HomeController
from assets.Assets_Management import AssetManager
from services.api.api_urls import API_ROUTES


class HomeUI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent" , corner_radius=15)
        self.Home_Ctrl = HomeController()
        self.pack(fill="both", expand=True)

        self.grid_rowconfigure(0, weight=7)
        self.grid_rowconfigure(1, weight=3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # # Frame 1: Biểu đồ cột
        # self.frame_bar = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=10)
        # self.frame_bar.grid(row=0, column=0, sticky="nsew", padx=(10,0), pady=10)
        # self.frame_bar.grid_rowconfigure(0, weight=1)
        # self.frame_bar.grid_columnconfigure(0, weight=1)

        # # Frame 2: Biểu đồ tròn
        # self.frame_pie = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=10)
        # self.frame_pie.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        # self.frame_pie.grid_rowconfigure(0, weight=1)
        # self.frame_pie.grid_columnconfigure(0, weight=1)

        # # # Hiển thị biểu đồ
        # self.Home_Ctrl.show_bar_chart(self.frame_bar)
        # self.Home_Ctrl.show_pie_chart(self.frame_pie)
        
        # # Frame 3: Số bệnh nhân trong tháng và nút Reload
        # # self.number_of_patient_in_month(self)
        # # self.button_reload(self)
        # # Frame 3: Thống kê bệnh nhân trong tháng + Reload
        # self.frame_info = ctk.CTkFrame(self, fg_color="#f8f9fa", border_width=2, border_color="#ccc", corner_radius=10)
        # self.frame_info.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))

        # self.label_patient_count = ctk.CTkLabel(
        #     self.frame_info,
        #     text="Đang tải dữ liệu...",
        #     font=ctk.CTkFont(size=18, weight="bold"),
        #     text_color="#212529"
        # )
        # self.label_patient_count.pack(side="left", padx=20, pady=20)

        # self.reload_button = ctk.CTkButton(
        #     self.frame_info,
        #     text="🔄 Tải lại",
        #     width=100,
        #     fg_color="#007bff",
        #     hover_color="#0056b3",
        #     command=self.reload_data
        # )
        # self.reload_button.pack(side="right", padx=20, pady=20)

        # # Hiển thị biểu đồ ban đầu
        # self.reload_data()
        
        
        # ============ FRAME 1: Biểu đồ cột (Nhóm tuổi) ============ #
        self.frame_bar = ctk.CTkFrame(
            self, fg_color="white", border_width=2,
            border_color="black", corner_radius=10
        )
        self.frame_bar.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        self.frame_bar.grid_rowconfigure(0, weight=1)
        self.frame_bar.grid_columnconfigure(0, weight=1)

        # ============ FRAME 2: Biểu đồ tròn (Giới tính) ============ #
        self.frame_pie = ctk.CTkFrame(
            self, fg_color="white", border_width=2,
            border_color="black", corner_radius=10
        )
        self.frame_pie.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_pie.grid_rowconfigure(0, weight=1)
        self.frame_pie.grid_columnconfigure(0, weight=1)

        # ============ FRAME 3: Thống kê bệnh nhân trong tháng ============ #
        self.frame_info = ctk.CTkFrame(
            self, fg_color="#f8f9fa", border_width=2,
            border_color="#ccc", corner_radius=10
        )
        self.frame_info.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))

        # Label hiển thị số bệnh nhân
        self.label_patient_count = ctk.CTkLabel(
            self.frame_info,
            text="Đang tải dữ liệu...",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#212529"
        )
        self.label_patient_count.pack(side="left", padx=20, pady=20)

        # Nút Reload
        self.reload_button = ctk.CTkButton(
            self.frame_info,
            text="🔄 Tải lại",
            width=120,
            fg_color="#007bff",
            hover_color="#0056b3",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.reload_data
        )
        self.reload_button.pack(side="right", padx=20, pady=20)

        # ============ TẢI DỮ LIỆU BAN ĐẦU ============ #
        self.reload_data()
        
    def reload_data(self):
        """Gọi API từ Controller và cập nhật giao diện"""
        # Xóa nội dung cũ
        for widget in self.frame_bar.winfo_children():
            widget.destroy()
        for widget in self.frame_pie.winfo_children():
            widget.destroy()

        # Gọi API và hiển thị lại biểu đồ
        self.Home_Ctrl.show_bar_chart(self.frame_bar)
        self.Home_Ctrl.show_pie_chart(self.frame_pie)

        # Gọi API lấy số lượng bệnh nhân trong tháng
        count = self.Home_Ctrl.get_patient_count_this_month()
        if count is not None:
            self.label_patient_count.configure(text=f"Số bệnh nhân trong tháng: {count}")
        else:
            self.label_patient_count.configure(text="⚠️ Không thể tải dữ liệu bệnh nhân.")

    def get_patient_count_this_month(self):
        try:
            url = API_ROUTES["statistics"]["month"]
            response = requests.get(url)
            data = response.json()
            return data.get("data", 0)
        except Exception as e:
            print("Lỗi khi tải dữ liệu bệnh nhân tháng:", e)
            return None

    
    #========= NUMBER OF PATIENT IN MONTH ==============
    def number_of_patient_in_month(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="white", border_width=2, border_color="black", corner_radius=10 )
        frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0,10))
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        frame.grid_columnconfigure(4, weight=1)
        frame.grid_columnconfigure(5, weight=1)
        frame.grid_columnconfigure(6, weight=1)
        frame.grid_columnconfigure(7, weight=1)

        # ========== Label tiêu đề ==========

        title = ctk.CTkLabel(frame,  text="Số lượng bệnh nhân trong tháng",text_color="black", font=ctk.CTkFont(size=14, weight="bold") , anchor="w", justify="left" , wraplength=100  )
        title.grid(row=0, column=0, padx=0, pady=10, sticky="ns")

        title = ctk.CTkLabel(frame, text="Tháng", text_color="black", font=ctk.CTkFont(size=14, weight="bold"), justify="left" , wraplength=100  )
        title.grid(row=0, column=2, padx=0, pady=10, sticky="ns")

        title = ctk.CTkLabel(frame, text="Năm", text_color="black", font=ctk.CTkFont(size=14, weight="bold"), justify="left" , wraplength=100  )
        title.grid(row=0, column=4, padx=0, pady=10, sticky="ns")

        # # ========== Ô số bệnh nhân ==========
        patient_box = ctk.CTkFrame(frame, fg_color="#42A5F5", corner_radius=8 , width=50, height=50 , border_width=2 , border_color="black")
        patient_box.grid_propagate(False)
        patient_box.grid(row=0, column=1, padx=0 , pady = 5 , sticky="nswe")
        number_label = ctk.CTkLabel(patient_box, text="145", font=ctk.CTkFont(size=28, weight="bold"), text_color="white")
        number_label.pack(expand=True, padx=5, pady=5)

        # # ========== Ô tháng ==========
        month_box = ctk.CTkFrame(frame, fg_color="#EF5350", corner_radius=8 ,width=50, height=50 , border_width=2 , border_color="black")
        month_box.grid_propagate(False)
        month_box.grid(row=0, column=3, pady=5, sticky="nswe")
        month_label = ctk.CTkLabel(month_box, text="7", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        month_label.place(relx=0.5, rely=0.5, anchor="center")

        # # ========== Ô năm ==========
        year_box = ctk.CTkFrame(frame, fg_color="#EF5350", corner_radius=8 , width=50, height=50 , border_width=2 , border_color="black")
        year_box.grid_propagate(False)
        year_box.grid(row=0, column=5, pady=5, sticky="nswe")
        year_label = ctk.CTkLabel(year_box, text="2025", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        year_label.pack(expand=True, padx=5, pady=5)

        # # ========== Link báo cáo lỗi ==========
        link = ctk.CTkLabel(frame, text="báo cáo lỗi ?", font=ctk.CTkFont(size=12, underline=True), text_color="blue", cursor="hand2")
        # Hover effect
        link.bind("<Enter>", lambda e: link.configure(text_color="red"))
        link.bind("<Leave>", lambda e: link.configure(text_color="blue"))

        # Gắn sự kiện click (ví dụ mở trình duyệt hoặc gọi hàm)
        link.bind("<Button-1>", lambda e: print("Đã nhấn vào Báo cáo lỗi"))

        link.grid(row=0, column=6, padx=10, pady=(0,5), sticky="s")

        #========== Nút reload ==========
        reload_button = self.button_reload(frame)
        reload_button.grid(row=0, column=7, padx=(0,10), pady=(0,5))

        return frame

    # ========== BUTTON RELOAD ==============
    def button_reload(self, parent):
        # ====== Load icon ======
        path_reload =  AssetManager.get_icon_path("btn_Refresh")  # đường dẫn icon của bạn
        reload_icon = Image.open(path_reload).resize((25, 25)) # kích thước icon
        reload_ctk = ctk.CTkImage(light_image=reload_icon, dark_image=reload_icon)

        # ====== Tạo nút hình tròn ======
        button = ctk.CTkButton(
            parent,
            image=reload_ctk,
            text="",  # không có chữ
            width=60,
            height=60,
            border_width=2,
            border_color="black",
            corner_radius=30,  # nửa chiều cao -> tròn
            fg_color="#F9C94F",
            hover_color="#45A049",
            command=lambda: print("Reload clicked!")
        )
        return button
