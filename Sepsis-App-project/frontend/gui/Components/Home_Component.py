import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HomeUI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent" , corner_radius=15)

        self.grid_rowconfigure(0, weight=7)
        self.grid_rowconfigure(1, weight=3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Frame 1: Biểu đồ cột
        self.frame_bar = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=10)
        self.frame_bar.grid(row=0, column=0, sticky="nsew", padx=(10,0), pady=10)
        self.frame_bar.grid_rowconfigure(0, weight=1)
        self.frame_bar.grid_columnconfigure(0, weight=1)

        # Frame 2: Biểu đồ tròn
        self.frame_pie = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=10)
        self.frame_pie.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_pie.grid_rowconfigure(0, weight=1)
        self.frame_pie.grid_columnconfigure(0, weight=1)

        # # Hiển thị biểu đồ
        # self.show_bar_chart(self.frame_bar)
        # self.show_pie_chart(self.frame_pie)
        
        # Frame 3: Số bệnh nhân trong tháng và nút Reload
        self.number_of_patient_in_month(self)
        self.button_reload(self)


    #========= SHOW CHARTS ==========
    def show_bar_chart(self, parent):
        x = ["A", "B", "C", "D"]
        y = [5, 7, 3, 8]

        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(x, y, color="skyblue")
        ax.set_title("Biểu đồ cột")
        ax.set_xlabel("Danh mục")
        ax.set_ylabel("Giá trị")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    #========= SHOW CHARTS ==========
    def show_pie_chart(self, parent):
        labels = ["A", "B", "C", "D"]
        sizes = [15, 30, 45, 10]

        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Biểu đồ tròn")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_pie_chart(self, parent):
        labels = ["A", "B", "C", "D"]
        sizes = [15, 30, 45, 10]

        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Biểu đồ tròn")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    #========= NUMBER OF PATIENT IN MONTH ==============
    def number_of_patient_in_month(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="white", border_width=2, border_color="black", corner_radius=10 )
        frame.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=(0,10))
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        # # ========== Label tiêu đề ==========
        # title = ctk.CTkLabel(frame, text="Số lượng bệnh nhân trong tháng", font=ctk.CTkFont(size=14, weight="bold"))
        # title.grid(row=0, column=0, padx=10, sticky="w")

        # # ========== Ô số bệnh nhân ==========
        # patient_box = ctk.CTkFrame(frame, fg_color="#42A5F5", corner_radius=8)
        # patient_box.grid(row=0, column=0, padx=5, sticky="nsew")
        # number_label = ctk.CTkLabel(patient_box, text="145", font=ctk.CTkFont(size=28, weight="bold"), text_color="white")
        # number_label.pack(padx=15, pady=(10, 0))
        # sub_label = ctk.CTkLabel(patient_box, text="Bệnh nhân", font=ctk.CTkFont(size=12), text_color="white")
        # sub_label.pack(pady=(0, 10))

        # # ========== Ô tháng ==========
        # month_box = ctk.CTkFrame(frame, fg_color="#EF5350", corner_radius=8)
        # month_box.grid(row=0, column=1, padx=5, sticky="nsew")
        # month_label = ctk.CTkLabel(month_box, text="7", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        # month_label.pack(padx=15, pady=(10, 0))
        # sub_month = ctk.CTkLabel(month_box, text="Tháng", font=ctk.CTkFont(size=12), text_color="white")
        # sub_month.pack(pady=(0, 10))

        # # ========== Ô năm ==========
        # year_box = ctk.CTkFrame(frame, fg_color="#EF5350", corner_radius=8)
        # year_box.grid(row=0, column=2, padx=5, sticky="nsew")
        # year_label = ctk.CTkLabel(year_box, text="2025", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        # year_label.pack(padx=15, pady=(10, 0))
        # sub_year = ctk.CTkLabel(year_box, text="Năm", font=ctk.CTkFont(size=12), text_color="white")
        # sub_year.pack(pady=(0, 10))

        # # ========== Link báo cáo lỗi ==========
        # link = ctk.CTkLabel(frame, text="báo cáo lỗi ?", font=ctk.CTkFont(size=12, underline=True), text_color="blue", cursor="hand2")
        # link.grid(row=1, padx=10, sticky="e")

        return frame

    # ========== BUTTON RELOAD ==============
    def button_reload(self, parent):
        button = ctk.CTkButton(
            parent,
            text="Reload",
            width=100,
            height=30,
            corner_radius=10,
            fg_color="#4CAF50",
            hover_color="#45A049",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: print("Reload clicked")
        )
        button.grid(row=1, column=1, sticky="e", padx=(0, 20), pady=(0, 10))
        return button
