import customtkinter as ctk
from matplotlib.figure import Figure
from PIL import Image , ImageTk , ImageDraw, ImageOps
from assets.Assets_Management import AssetManager
import tkinter as tk
from tkinter import ttk

class Patient_UI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        # Cấu hình grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_columnconfigure(0, weight=1)

        # ========== ROW 0: 3 columns ==========
        self.create_row0()
        
        # ========== ROW 1: Table với scroll ==========
        self.create_patient_table()

    def create_row0(self):
        """Tạo row 0 với 3 columns."""
        row0_frame = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=10)
        row0_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10,5))
        
        # Cấu hình grid cho row0_frame
        row0_frame.grid_columnconfigure(0, weight=1)
        row0_frame.grid_columnconfigure(1, weight=1)
        row0_frame.grid_columnconfigure(2, weight=1)
        
        # Column 0 - Dropdown lọc theo cột
        col0_frame = ctk.CTkFrame(row0_frame, fg_color="#F7F7F5", corner_radius=10)
        col0_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Label tiêu đề
        label0 = ctk.CTkLabel(col0_frame, text="Lọc theo cột", font=ctk.CTkFont(size=12, weight="bold"), text_color="black")
        label0.pack(pady=(10,5))
        
        # Dropdown menu
        self.filter_column = ctk.StringVar(value="Tất cả")
        column_options = ["Tất cả", "STT", "ID", "Họ và tên", "Ngày sinh", "Giới tính", "SDT", "Email"]
        
        self.column_dropdown = ctk.CTkOptionMenu(
            col0_frame,
            variable=self.filter_column,
            values=column_options,
            font=ctk.CTkFont(size=11),
            dropdown_font=ctk.CTkFont(size=11),
            width=150,
            height=30,
            corner_radius=10,
            fg_color="#66B7FF",
            button_color="#66B7FF",
            button_hover_color="#45a049",
            dropdown_fg_color="#F7F7F5",
            dropdown_hover_color="#66B7FF",
            command=self.on_column_filter_change
        )
        self.column_dropdown.pack(pady=(0,10))
        
        # Column 1 - Search box
        col1_frame = ctk.CTkFrame(row0_frame, fg_color="#F7F7F5", corner_radius=10)
        col1_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Label tiêu đề
        label1 = ctk.CTkLabel(col1_frame, text="Tìm kiếm bệnh nhân", font=ctk.CTkFont(size=12, weight="bold"), text_color="black")
        label1.pack(pady=(10,5))
        
        # Frame chứa search box và button
        search_container = ctk.CTkFrame(col1_frame, fg_color="transparent")
        search_container.pack(pady=(0,10), padx=10)
        
        # Entry tìm kiếm
        self.search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="Nhập ID, tên, SĐT...",
            font=ctk.CTkFont(size=11),
            width=200,
            height=30,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="white"
        )
        self.search_entry.pack(side="left", padx=(0,5))
        
        # Button tìm kiếm với icon kính lúp
        try:
            search_icon_path = AssetManager.get_icon_path("btn_search")
            search_icon = ctk.CTkImage(
                light_image=Image.open(search_icon_path),
                dark_image=Image.open(search_icon_path),
                size=(20, 20)
            )
            
            self.search_button = ctk.CTkButton(
                search_container,
                text="",
                image=search_icon,
                width=30,
                height=30,
                corner_radius=5,
                fg_color="#66B7FF",
                hover_color="#45a049",
                border_width=2,
                border_color="black",
                command=self.on_search_click
            )
        except:
            # Fallback nếu không tìm thấy icon
            self.search_button = ctk.CTkButton(
                search_container,
                text="🔍",
                width=30,
                height=30,
                corner_radius=5,
                fg_color="#66B7FF",
                hover_color="#45a049",
                border_width=2,
                border_color="black",
                font=ctk.CTkFont(size=14),
                command=self.on_search_click
            )
        
        self.search_button.pack(side="left")
        
        # Bind Enter key cho search
        self.search_entry.bind("<Return>", lambda event: self.on_search_click())
        
        # Column 2 - Nút thêm/xóa bệnh nhân
        col2_frame = ctk.CTkFrame(row0_frame, fg_color="#F7F7F5", corner_radius=10)
        col2_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Label tiêu đề
        label2 = ctk.CTkLabel(col2_frame, text="Thao tác", font=ctk.CTkFont(size=12, weight="bold"), text_color="black")
        label2.pack(pady=(10,5))
        
        # Frame chứa 2 nút
        buttons_container = ctk.CTkFrame(col2_frame, fg_color="transparent")
        buttons_container.pack(pady=(0,10))
        
        # Nút + (Thêm bệnh nhân)
        self.add_button = ctk.CTkButton(
            buttons_container,
            text="+",
            width=40,
            height=40,
            corner_radius=5,
            fg_color="#4CAF50",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self.on_add_patient
        )
        self.add_button.pack(side="left", padx=5)
        
        # Nút - (Xóa bệnh nhân)
        self.delete_button = ctk.CTkButton(
            buttons_container,
            text="-",
            width=40,
            height=40,
            corner_radius=5,
            fg_color="#F44336",
            hover_color="#da190b",
            border_width=2,
            border_color="black",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self.on_delete_patient
        )
        self.delete_button.pack(side="left", padx=5)

    def create_patient_table(self):
        """Tạo table hiển thị danh sách bệnh nhân với scrollbar."""
        table_frame = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=10)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5,10))
        
        # Cấu hình grid
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Tạo Treeview với scrollbar
        tree_container = ctk.CTkFrame(table_frame, fg_color="white")
        tree_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Scrollbar dọc
        scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        
        # Scrollbar ngang
        scrollbar_x = ttk.Scrollbar(tree_container, orient="horizontal")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Treeview (Table)
        columns = ("STT", "ID", "Họ và tên", "Ngày sinh", "Giới tính", "SDT", "Email", "Tác vụ")
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            height=15
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Kết nối scrollbar với treeview
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Cấu hình tiêu đề cột
        self.tree.heading("STT", text="STT")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Họ và tên", text="Họ và tên")
        self.tree.heading("Ngày sinh", text="Ngày sinh")
        self.tree.heading("Giới tính", text="Giới tính")
        self.tree.heading("SDT", text="SDT")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Tác vụ", text="Tác vụ")
        
        # Cấu hình độ rộng cột
        self.tree.column("STT", width=50, anchor="center")
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Họ và tên", width=150, anchor="w")
        self.tree.column("Ngày sinh", width=100, anchor="center")
        self.tree.column("Giới tính", width=80, anchor="center")
        self.tree.column("SDT", width=120, anchor="center")
        self.tree.column("Email", width=180, anchor="w")
        self.tree.column("Tác vụ", width=100, anchor="center")
        
        # Style cho Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
            background="white",
            foreground="black",
            rowheight=30,
            fieldbackground="white",
            font=("Roboto", 11)
        )
        style.configure("Treeview.Heading",
            background="#66B7FF",
            foreground="white",
            font=("Roboto", 12, "bold"),
            borderwidth=2,
            relief="raised"
        )
        style.map("Treeview",
            background=[("selected", "#66B7FF")]
        )
        
        # Thêm dữ liệu mẫu (có thể xóa sau)
        sample_data = [
            ("1", "BN001", "Nguyễn Văn A", "01/01/1990", "Nam", "0901234567", "nguyenvana@email.com", "Xem/Sửa/Xóa"),
            ("2", "BN002", "Trần Thị B", "15/05/1985", "Nữ", "0912345678", "tranthib@email.com", "Xem/Sửa/Xóa"),
            ("3", "BN003", "Lê Văn C", "20/08/1992", "Nam", "0923456789", "levanc@email.com", "Xem/Sửa/Xóa"),
            ("4", "BN004", "Phạm Thị D", "10/12/1988", "Nữ", "0934567890", "phamthid@email.com", "Xem/Sửa/Xóa"),
            ("5", "BN005", "Hoàng Văn E", "25/03/1995", "Nam", "0945678901", "hoangvane@email.com", "Xem/Sửa/Xóa"),
        ]
        
        for data in sample_data:
            self.tree.insert("", "end", values=data)
    
    def on_column_filter_change(self, selected_column):
        """Xử lý khi người dùng chọn cột để lọc."""
        print(f"🔍 Lọc theo cột: {selected_column}")
        
        # Lưu lại tất cả columns ban đầu
        all_columns = ("STT", "ID", "Họ và tên", "Ngày sinh", "Giới tính", "SDT", "Email", "Tác vụ")
        
        if selected_column == "Tất cả":
            # Hiển thị tất cả các cột
            self.tree["displaycolumns"] = all_columns
        else:
            # Hiển thị cột được chọn + STT + Tác vụ (để user vẫn biết thứ tự và thao tác)
            if selected_column == "STT":
                self.tree["displaycolumns"] = ("STT", "Tác vụ")
            elif selected_column in all_columns:
                # Hiển thị: STT + cột được chọn + Tác vụ
                self.tree["displaycolumns"] = ("STT", selected_column, "Tác vụ")
            else:
                self.tree["displaycolumns"] = all_columns
        
        print(f"✅ Hiển thị các cột: {self.tree['displaycolumns']}")
    
    def on_search_click(self):
        """Xử lý khi người dùng click nút tìm kiếm."""
        search_text = self.search_entry.get().strip().lower()
        print(f"🔍 Tìm kiếm: {search_text}")
        
        if not search_text:
            # Nếu search rỗng, hiển thị lại tất cả
            for item in self.tree.get_children():
                self.tree.reattach(item, '', 'end')
            print("✅ Hiển thị tất cả dữ liệu")
            return
        
        # Lọc dữ liệu theo search text
        matched_items = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            # Tìm trong tất cả các cột (chuyển về lowercase để so sánh)
            item_text = ' '.join(str(v).lower() for v in values)
            
            if search_text in item_text:
                matched_items.append(item)
        
        # Xóa tất cả items hiện tại
        for item in self.tree.get_children():
            self.tree.detach(item)
        
        # Chỉ hiển thị items khớp
        for item in matched_items:
            self.tree.reattach(item, '', 'end')
        
        print(f"✅ Tìm thấy {len(matched_items)} kết quả")
    
    def on_add_patient(self):
        """Xử lý khi người dùng click nút thêm bệnh nhân (+)."""
        print("➕ Nút thêm bệnh nhân được click")
        # TODO: Implement thêm bệnh nhân mới
        pass
    
    def on_delete_patient(self):
        """Xử lý khi người dùng click nút xóa bệnh nhân (-)."""
        # Kiểm tra xem có bệnh nhân nào được chọn không
        selected_items = self.tree.selection()
        
        if not selected_items:
            # Hiển thị thông báo nếu chưa chọn bệnh nhân
            self.show_warning_popup("Vui lòng chọn bệnh nhân cần xóa!")
            return
        
        # Lấy thông tin bệnh nhân được chọn
        selected_item = selected_items[0]
        patient_data = self.tree.item(selected_item)['values']
        patient_name = patient_data[2]  # Họ và tên ở cột index 2
        patient_id = patient_data[1]    # ID ở cột index 1
        
        print(f"🗑️ Yêu cầu xóa bệnh nhân: {patient_name} (ID: {patient_id})")
        
        # Hiển thị popup xác nhận
        self.show_confirm_delete_popup(selected_item, patient_name)
    
    def show_warning_popup(self, message):
        """Hiển thị popup cảnh báo."""
        popup = ctk.CTkToplevel(self)
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
    
    def show_confirm_delete_popup(self, item_id, patient_name):
        """Hiển thị popup xác nhận xóa bệnh nhân."""
        popup = ctk.CTkToplevel(self)
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
            command=lambda: self.confirm_delete(popup, item_id, patient_name)
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
    
    def confirm_delete(self, popup, item_id, patient_name):
        """Xác nhận và thực hiện xóa bệnh nhân."""
        # Xóa bệnh nhân khỏi table
        self.tree.delete(item_id)
        print(f"✅ Đã xóa bệnh nhân: {patient_name}")
        
        # TODO: Gọi API backend để xóa bệnh nhân khỏi database
        
        # Đóng popup
        popup.destroy()

 
