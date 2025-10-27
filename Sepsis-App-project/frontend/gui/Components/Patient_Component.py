import customtkinter as ctk
from matplotlib.figure import Figure
from PIL import Image , ImageTk , ImageDraw, ImageOps
from assets.Assets_Management import AssetManager
import tkinter as tk
from tkinter import ttk
from controllers.Patient_Controller import PatientController
from gui.Components.Patient_Detail_Component import PatientDetailPopups

class Patient_UI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        # Khởi tạo controller
        self.controller = PatientController()
        
        # Khởi tạo popups manager
        self.popups = PatientDetailPopups(self, self.controller)

        # Cấu hình grid - Row 0 tự động điều chỉnh theo nội dung, Row 1 chiếm phần còn lại
        self.grid_rowconfigure(0, weight=0)  # Row 0 tự động theo nội dung (không co giãn)
        self.grid_rowconfigure(1, weight=1)  # Row 1 tự động mở rộng chiếm phần còn lại
        self.grid_columnconfigure(0, weight=1)

        # ========== ROW 0: 3 columns ==========
        self.create_row0()
        
        # ========== ROW 1: Table với scroll ==========
        self.create_patient_table()

    def create_row0(self):
        """Tạo row 0 với 3 columns."""
        row0_frame = ctk.CTkFrame(self, fg_color="transparent")
        row0_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,5))
        # Bỏ grid_propagate(False) để frame tự động điều chỉnh theo nội dung
        
        # Cấu hình grid cho row0_frame
        row0_frame.grid_columnconfigure(0, weight=1)
        row0_frame.grid_columnconfigure(1, weight=1)
        row0_frame.grid_columnconfigure(2, weight=1)
        
        # Column 0 - Dropdown lọc theo cột
        col0_frame = ctk.CTkFrame(row0_frame, fg_color="transparent", corner_radius=10 )
        col0_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        
        # Dropdown menu
        self.filter_column = ctk.StringVar(value="Tất cả")
        column_options = ["Tất cả", "STT", "ID", "Họ và tên", "Ngày sinh", "Giới tính", "SDT", "Email"]
        
        self.column_dropdown = ctk.CTkOptionMenu(
            col0_frame,
            variable=self.filter_column,
            values=column_options,
            font=ctk.CTkFont(size=11, weight="bold"),
            dropdown_font=ctk.CTkFont(size=11, weight="bold"),
            width=150,
            height=40,
            corner_radius=10,
            text_color="black",
            fg_color="#66B7FF",
            button_color="#66B7FF",
            button_hover_color="#45a049",
            dropdown_text_color="black",
            dropdown_fg_color="#F7F7F5",
            dropdown_hover_color="#66B7FF",
            command=self.on_column_filter_change
        )
        self.column_dropdown.pack(pady=(0,10))
        
        # Column 1 - Search box
        col1_frame = ctk.CTkFrame(row0_frame, fg_color="transparent", corner_radius=10)
        col1_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Frame chứa search box và button
        search_container = ctk.CTkFrame(col1_frame, fg_color="transparent")
        search_container.pack(pady=(0,10), padx=10)
        
        # Entry tìm kiếm
        self.search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="Nhập ID, tên, SĐT...",
            font=ctk.CTkFont(size=11),
            width=300,
            height=40,
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
                width=40,
                height=40,
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
                width=40,
                height=40,
                corner_radius=10,
                fg_color="#66B7FF",
                hover_color="#45a049",
                border_width=2,
                border_color="black",
                font=ctk.CTkFont(size=20, weight="bold"),
                command=self.on_search_click
            )
        
        self.search_button.pack(side="left")
        
        # Bind Enter key cho search
        self.search_entry.bind("<Return>", lambda event: self.on_search_click())
        
        # Column 2 - Nút thêm/xóa bệnh nhân
        col2_frame = ctk.CTkFrame(row0_frame, fg_color="transparent", corner_radius=10)
        col2_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Frame chứa 2 nút
        buttons_container = ctk.CTkFrame(col2_frame, fg_color="transparent")
        buttons_container.pack(pady=(0,10))
        
        # Nút + (Thêm bệnh nhân)
        self.add_button = ctk.CTkButton(
            buttons_container,
            text="+",
            width=40,
            height=40,
            corner_radius=10,
            fg_color="#66B7FF",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            font=ctk.CTkFont(size=30, weight="bold" , family="Roboto"),
            command=self.on_add_patient
        )
        self.add_button.pack(side="left", padx=5)
        
        # Nút - (Xóa bệnh nhân)
        self.delete_button = ctk.CTkButton(
            buttons_container,
            text="-",
            width=40,
            height=40,
            corner_radius=10,
            fg_color="#66B7FF",
            hover_color="#45a049",
            border_width=2,
            border_color="black",
            font=ctk.CTkFont(size=30, weight="bold" , family="Roboto"),
            command=self.on_delete_patient
        )
        self.delete_button.pack(side="left", padx=5)

    def create_patient_table(self):
        """Tạo table hiển thị danh sách bệnh nhân với scrollbar."""
        # Frame ngoài với viền và bo góc
        table_frame = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="black", corner_radius=15)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5,10))
        
        # Cấu hình grid
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Container bên trong với bo góc và clip content
        tree_container = ctk.CTkFrame(table_frame, fg_color="white", corner_radius=15)
        tree_container.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Scrollbar dọc
        scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        
        # Scrollbar ngang
        scrollbar_x = ttk.Scrollbar(tree_container, orient="horizontal")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Treeview (Table) - Thêm lại cột "Tác vụ" để hiển thị text "Xem chi tiết"
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
        self.tree.column("Tác vụ", width=130, anchor="center")
        
        # Style cho Treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        # Bỏ viền các ô dữ liệu
        style.configure("Treeview",
            background="white",
            foreground="black",
            rowheight=40,
            fieldbackground="white",
            font=("Roboto", 11),
            borderwidth=0,  # Bỏ viền ô
            relief="flat",  # Không có relief effect
            highlightthickness=0  # Bỏ viền khi focus
        )
        
        # Tiêu đề cột: style với viền dưới
        style.configure("Treeview.Heading",
            background="#66B7FF",
            foreground="white",
            font=("Roboto", 12, "bold"),
            relief="flat"       # Flat style
        )
        
        # Màu khi selected - màu nhạt để dễ nhìn
        style.map("Treeview",
            background=[("selected", "#E3F2FD")],  # Màu xanh nhạt khi chọn
            foreground=[("selected", "black")]
        )
        
        # Map cho heading - hover effect
        style.map("Treeview.Heading",
            background=[("active", "#5aa3e0")],
            foreground=[("active", "white")],
            relief=[("active", "flat")]
        )
        
        # Thêm dữ liệu mẫu - Thêm text "Xem chi tiết" vào cột cuối
        sample_data = [
                ("1", "BN001", "Nguyễn Văn A", "01/01/1990", "Nam", "0901234567", "nguyenvana@email.com", "📋 Xem chi tiết"),
                ("2", "BN002", "Trần Thị B", "15/05/1985", "Nữ", "0912345678", "tranthib@email.com", "📋 Xem chi tiết"),
                ("3", "BN003", "Lê Văn C", "20/08/1992", "Nam", "0923456789", "levanc@email.com", "📋 Xem chi tiết"),
                ("4", "BN004", "Phạm Thị D", "10/12/1988", "Nữ", "0934567890", "phamthid@email.com", "📋 Xem chi tiết"),
                ("5", "BN005", "Hoàng Văn E", "25/03/1995", "Nam", "0945678901", "hoangvane@email.com", "📋 Xem chi tiết"),
                ("6", "BN006", "Võ Thị F", "12/07/1993", "Nữ", "0956789012", "vothif@email.com", "📋 Xem chi tiết"),
                ("7", "BN007", "Đặng Văn G", "30/11/1987", "Nam", "0967890123", "dangvang@email.com", "📋 Xem chi tiết"),
                ("8", "BN008", "Mai Thị H", "18/02/1991", "Nữ", "0978901234", "maithih@email.com", "📋 Xem chi tiết"),
                ("9", "BN009", "Ngô Văn I", "09/09/1989", "Nam", "0989012345", "ngovani@email.com", "📋 Xem chi tiết"),
                ("10", "BN010", "Lý Thị K", "05/06/1994", "Nữ", "0990123456", "lythik@email.com", "📋 Xem chi tiết"),
                ("11", "BN011", "Tạ Văn L", "14/04/1990", "Nam", "0902345678", "tavanl@email.com", "📋 Xem chi tiết"),
                ("12", "BN012", "Phan Thị M", "22/08/1992", "Nữ", "0913456789", "phanthim@email.com", "📋 Xem chi tiết"),
                ("13", "BN013", "Đỗ Văn N", "30/10/1986", "Nam", "0924567890", "dovann@email.com", "📋 Xem chi tiết"),
                ("14", "BN014", "Nguyễn Thị O", "08/03/1991", "Nữ", "0935678901", "nguyenthio@email.com", "📋 Xem chi tiết"),
                ("15", "BN015", "Bùi Văn P", "27/11/1993", "Nam", "0946789012", "buivanp@email.com", "📋 Xem chi tiết"),
                ("16", "BN016", "Trịnh Thị Q", "19/07/1990", "Nữ", "0957890123", "trinhthiq@email.com", "📋 Xem chi tiết"),
                ("17", "BN017", "Nguyễn Văn R", "02/02/1988", "Nam", "0968901234", "nguyenvanr@email.com", "📋 Xem chi tiết"),
                ("18", "BN018", "Lâm Thị S", "23/09/1995", "Nữ", "0979012345", "lamthis@email.com", "📋 Xem chi tiết"),
                ("19", "BN019", "Phùng Văn T", "17/05/1992", "Nam", "0980123456", "phungvant@email.com", "📋 Xem chi tiết"),
                ("20", "BN020", "Đoàn Thị U", "04/12/1989", "Nữ", "0991234567", "doanthiu@email.com", "📋 Xem chi tiết"),
        ]
        
        for data in sample_data:
            self.tree.insert("", "end", values=data)
        
        # Bind double-click vào cột "Tác vụ" để xem chi tiết
        self.tree.bind('<Double-Button-1>', self.on_tree_double_click)
        
        # Tag để tô màu cột Tác vụ giống button
        self.tree.tag_configure('action', foreground='#2e7d32', font=('Roboto', 11, 'bold'))
        
    def on_tree_double_click(self, event):
        """Xử lý khi double-click vào một dòng trong bảng."""
        # Lấy item được click
        item = self.tree.identify('item', event.x, event.y)
        if not item:
            return
        
        # Lấy column được click
        column = self.tree.identify_column(event.x)
        
        # Lấy dữ liệu của dòng
        values = self.tree.item(item, 'values')
        if not values:
            return
        
        # Nếu click vào cột "Tác vụ" hoặc bất kỳ cột nào, hiển thị chi tiết
        # Column #8 là cột "Tác vụ" (index bắt đầu từ #1)
        patient_data = values[:7]  # Lấy 7 cột đầu (không lấy cột "Tác vụ")
        
        # Sử dụng popups manager để hiển thị chi tiết
        self.popups.show_patient_detail(
            patient_data,
            on_edit_callback=self.edit_patient,
            on_delete_callback=self.delete_from_detail
        )
    
    # ==================== CALLBACK METHODS ====================
    
    def edit_patient(self, patient_data):
        """Callback khi nhấn nút Sửa từ popup chi tiết."""
        print(f"✏️ Chỉnh sửa: {patient_data[2]}")
        self.popups.show_edit_patient_form(patient_data, self.save_edit_patient)
    
    def delete_from_detail(self, patient_data):
        """Callback khi nhấn nút Xóa từ popup chi tiết."""
        # Tìm item_id từ patient_data
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id)['values']
            if values[1] == patient_data[1]:  # So sánh ID
                patient_name = patient_data[2]
                self.popups.show_confirm_delete_popup(
                    patient_name,
                    on_confirm_callback=lambda popup: self.confirm_delete(popup, item_id, patient_name)
                )
                break
    
    def on_column_filter_change(self, selected_column):
        """Xử lý khi người dùng chọn cột để lọc."""
        print(f"🔍 Lọc theo cột: {selected_column}")
        
        # Gọi controller để lấy cột hiển thị
        display_columns, _ = self.controller.filter_by_column(selected_column, [])
        self.tree["displaycolumns"] = display_columns
        
        print(f"✅ Hiển thị các cột: {self.tree['displaycolumns']}")
    
    def on_search_click(self):
        """Xử lý khi người dùng click nút tìm kiếm."""
        search_text = self.search_entry.get().strip()
        print(f"🔍 Tìm kiếm: {search_text}")
        
        if not search_text:
            # Nếu search rỗng, hiển thị lại tất cả
            for item in self.tree.get_children():
                self.tree.reattach(item, '', 'end')
            print("✅ Hiển thị tất cả dữ liệu")
            return
        
        # Lấy danh sách tất cả bệnh nhân từ tree
        all_patients = []
        item_map = {}  # Map patient_id -> tree_item_id
        
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            patient = {
                'id': values[1],
                'full_name': values[2],
                'birth_date': values[3],
                'gender': values[4],
                'phone': values[5],
                'email': values[6]
            }
            all_patients.append(patient)
            item_map[values[1]] = item
        
        # Gọi controller để tìm kiếm
        matched_patients = self.controller.search_patients(search_text, all_patients)
        matched_ids = {p['id'] for p in matched_patients}
        
        # Detach tất cả items
        for item in self.tree.get_children():
            self.tree.detach(item)
        
        # Reattach chỉ các items khớp
        for patient_id in matched_ids:
            if patient_id in item_map:
                self.tree.reattach(item_map[patient_id], '', 'end')
        
        print(f"✅ Tìm thấy {len(matched_patients)} kết quả")
    
    def on_add_patient(self):
        """Xử lý khi người dùng click nút thêm bệnh nhân (+)."""
        print("➕ Nút thêm bệnh nhân được click")
        self.popups.show_add_patient_form(self.save_new_patient)
    
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
        
        # Hiển thị popup xác nhận qua popups manager
        self.popups.show_confirm_delete_popup(
            patient_name,
            on_confirm_callback=lambda popup: self.confirm_delete(popup, selected_item, patient_name)
        )
    
    def confirm_delete(self, popup, item_id, patient_name):
        """Xác nhận và thực hiện xóa bệnh nhân."""
        # Lấy patient_id từ tree item
        values = self.tree.item(item_id)['values']
        patient_id = values[1]
        
        # Gọi controller để xóa bệnh nhân
        success, message = self.controller.delete_patient(patient_id)
        
        if success:
            # Xóa khỏi table nếu API thành công
            self.tree.delete(item_id)
            print(f"✅ Đã xóa bệnh nhân: {patient_name}")
        else:
            # Hiển thị lỗi nếu thất bại
            self.popups.show_warning_popup(f"Lỗi: {message}")
        
        # Đóng popup
        popup.destroy()
    
    # ==================== SAVE METHODS ====================
    
    def save_new_patient(self, fields, popup):
        """Lưu bệnh nhân mới."""
        # Lấy dữ liệu từ form
        patient_data = {
            'full_name': fields['full_name'].get().strip(),
            'birth_date': fields['birth_date'].get().strip(),
            'gender': fields['gender'].get(),
            'phone': fields['phone'].get().strip(),
            'email': fields['email'].get().strip()
        }
        
        # Validate
        is_valid, error_message = self.controller.validate_patient_data(patient_data)
        if not is_valid:
            self.popups.show_warning_popup(error_message)
            return
        
        # Gọi API để tạo bệnh nhân
        success, message, data = self.controller.create_patient(patient_data)
        
        if success:
            # Thêm vào table
            new_stt = len(self.tree.get_children()) + 1
            new_row = (
                str(new_stt),
                data.get('id', ''),
                patient_data['full_name'],
                patient_data['birth_date'],
                patient_data['gender'],
                patient_data['phone'],
                patient_data['email'],
                "📋 Xem chi tiết"
            )
            self.tree.insert("", "end", values=new_row)
            print(f"✅ Đã thêm bệnh nhân: {patient_data['full_name']}")
            popup.destroy()
        else:
            self.popups.show_warning_popup(f"Lỗi: {message}")
    
    def save_edit_patient(self, patient_id, fields, popup):
        """Lưu thay đổi bệnh nhân."""
        # Lấy dữ liệu từ form
        patient_data = {
            'full_name': fields['full_name'].get().strip(),
            'birth_date': fields['birth_date'].get().strip(),
            'gender': fields['gender'].get(),
            'phone': fields['phone'].get().strip(),
            'email': fields['email'].get().strip()
        }
        
        # Validate
        is_valid, error_message = self.controller.validate_patient_data(patient_data)
        if not is_valid:
            self.popups.show_warning_popup(error_message)
            return
        
        # Gọi API để cập nhật
        success, message, data = self.controller.update_patient(patient_id, patient_data)
        
        if success:
            # Cập nhật trong table
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                if values[1] == patient_id:
                    updated_row = (
                        values[0],  # Giữ nguyên STT
                        patient_id,
                        patient_data['full_name'],
                        patient_data['birth_date'],
                        patient_data['gender'],
                        patient_data['phone'],
                        patient_data['email'],
                        "📋 Xem chi tiết"
                    )
                    self.tree.item(item, values=updated_row)
                    break
            
            print(f"✅ Đã cập nhật bệnh nhân: {patient_data['full_name']}")
            popup.destroy()
        else:
            self.popups.show_warning_popup(f"Lỗi: {message}")


 
