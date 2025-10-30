import customtkinter as ctk
from tkinter import ttk
from controllers.Employee_Controller import EmployeeController
from gui.Components.Employee_Detail_Component import EmployeeDetail
from gui.Components.Employee_Forms_Component import EmployeeForms
from gui.Components.Employee_Dialogs_Component import EmployeeDialogs

class Employee_UI(ctk.CTkFrame):
    """Giao diện quản lý nhân viên."""
    
    def __init__(self, master, controller=None):
        super().__init__(master, fg_color="transparent")
        
        self.controller = EmployeeController()
        
        # Khởi tạo các component con
        self.detail_popup = EmployeeDetail(self)
        self.forms = EmployeeForms(self)
        self.dialogs = EmployeeDialogs(self)
        
        self.pack(fill="both", expand=True)
        
        # Tạo giao diện
        self.create_widgets()
        
        # Load dữ liệu ban đầu
        self.load_employees()
    
    # ==================== CREATE WIDGETS ====================
    
    def create_widgets(self):
        """Tạo các widget cho giao diện."""
        
        # ========== HEADER ==========
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="QUẢN LÝ NHÂN VIÊN",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#66B7FF"
        )
        title_label.pack(side="left")
        
        # ========== SEARCH & FILTER FRAME ==========
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        # Label "Lọc theo"
        filter_label = ctk.CTkLabel(
            search_frame,
            text="Lọc theo:",
            font=ctk.CTkFont(size=14)
        )
        filter_label.pack(side="left", padx=(0, 10))
        
        # Combobox lọc theo cột
        self.filter_column = ctk.CTkComboBox(
            search_frame,
            values=["Tất cả", "ID", "Họ và tên", "Giới tính", "SDT", "Email", "Chức vụ", "Phòng ban"],
            width=150,
            command=self.on_filter_change
        )
        self.filter_column.set("Tất cả")
        self.filter_column.pack(side="left", padx=(0, 20))
        
        # Entry tìm kiếm
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Tìm kiếm nhân viên...",
            width=300
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Nút Tìm kiếm
        search_button = ctk.CTkButton(
            search_frame,
            text="Tìm kiếm",
            width=100,
            fg_color="#66B7FF",
            hover_color="#45a049",
            command=self.search_employees
        )
        search_button.pack(side="left", padx=(0, 10))
        
        # Nút Làm mới
        refresh_button = ctk.CTkButton(
            search_frame,
            text="Làm mới",
            width=100,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self.load_employees
        )
        refresh_button.pack(side="left")
        
        # ========== TABLE FRAME ==========
        table_frame = ctk.CTkFrame(self, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tạo Treeview với style tùy chỉnh
        style = ttk.Style()
        style.theme_use("clam")
        
        # Tùy chỉnh Treeview
        style.configure(
            "Custom.Treeview",
            background="white",
            foreground="black",
            rowheight=35,
            fieldbackground="white",
            borderwidth=0,
            relief="flat"
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "#66B7FF")],
            foreground=[("selected", "white")]
        )
        
        # Tùy chỉnh header
        style.configure(
            "Custom.Treeview.Heading",
            background="#66B7FF",
            foreground="white",
            borderwidth=0,
            relief="flat",
            font=("Arial", 11, "bold")
        )
        style.map(
            "Custom.Treeview.Heading",
            background=[("active", "#45a049")]
        )
        
        # Tạo Treeview
        columns = ("STT", "ID", "Họ và tên", "Ngày sinh", "Giới tính", "SDT", "Email", "Tác vụ")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )
        
        # Định nghĩa các cột
        column_widths = {
            "STT": 50,
            "ID": 80,
            "Họ và tên": 180,
            "Ngày sinh": 100,
            "Giới tính": 80,
            "SDT": 110,
            "Email": 200,
            "Tác vụ": 150
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree và scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click để xem chi tiết
        self.tree.bind("<Double-Button-1>", self.on_row_double_click)
        
        # ========== BUTTON FRAME ==========
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # Nút Thêm nhân viên
        add_button = ctk.CTkButton(
            button_frame,
            text="➕ Thêm nhân viên mới",
            width=180,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_add_employee_form
        )
        add_button.pack(side="left", padx=(0, 10))
        
        # Nút Xóa nhân viên đã chọn
        delete_button = ctk.CTkButton(
            button_frame,
            text="🗑️ Xóa nhân viên",
            width=150,
            height=40,
            fg_color="#F44336",
            hover_color="#da190b",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.delete_selected_employee
        )
        delete_button.pack(side="left")
    
    # ==================== LOAD DATA ====================
    
    def load_employees(self):
        """Load danh sách nhân viên từ database."""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # TODO: Lấy dữ liệu từ API
        # employees = self.controller.get_all_employees()
        
        # Giả lập dữ liệu mẫu
        sample_employees = [
            ("NV001", "Nguyễn Văn A", "01/01/1990", "Nam", "0123456789", "nguyenvana@example.com"),
            ("NV002", "Trần Thị B", "15/05/1992", "Nữ", "0987654321", "tranthib@example.com"),
            ("NV003", "Lê Văn C", "20/10/1988", "Nam", "0345678901", "levanc@example.com"),
            ("NV004", "Phạm Thị D", "08/03/1995", "Nữ", "0912345678", "phamthid@example.com"),
            ("NV005", "Hoàng Văn E", "12/07/1991", "Nam", "0778899001", "hoangvane@example.com"),
        ]
        
        for idx, emp in enumerate(sample_employees, start=1):
            emp_id, name, birth_date, gender, phone, email = emp
            self.tree.insert(
                "",
                "end",
                values=(idx, emp_id, name, birth_date, gender, phone, email, "👁️ Xem | ✏️ Sửa | 🗑️ Xóa"),
                tags=("data",)
            )
        
        # Thêm alternating row colors
        self.tree.tag_configure("data", background="white")
        for idx, item in enumerate(self.tree.get_children()):
            if idx % 2 == 1:
                self.tree.item(item, tags=("oddrow",))
        self.tree.tag_configure("oddrow", background="#F0F0F0")
    
    # ==================== SEARCH & FILTER ====================
    
    def on_filter_change(self, choice):
        """Xử lý khi thay đổi filter."""
        self.search_employees()
    
    def on_search(self, event):
        """Xử lý khi gõ vào ô tìm kiếm."""
        self.search_employees()
    
    def search_employees(self):
        """Tìm kiếm và lọc nhân viên."""
        search_text = self.search_entry.get().strip().lower()
        filter_col = self.filter_column.get()
        
        # Xóa dữ liệu hiện tại
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # TODO: Gọi API với filter và search
        # employees = self.controller.search_employees(search_text, filter_col)
        
        # Giả lập tìm kiếm trên dữ liệu mẫu
        sample_employees = [
            ("NV001", "Nguyễn Văn A", "01/01/1990", "Nam", "0123456789", "nguyenvana@example.com"),
            ("NV002", "Trần Thị B", "15/05/1992", "Nữ", "0987654321", "tranthib@example.com"),
            ("NV003", "Lê Văn C", "20/10/1988", "Nam", "0345678901", "levanc@example.com"),
            ("NV004", "Phạm Thị D", "08/03/1995", "Nữ", "0912345678", "phamthid@example.com"),
            ("NV005", "Hoàng Văn E", "12/07/1991", "Nam", "0778899001", "hoangvane@example.com"),
        ]
        
        filtered_employees = []
        for emp in sample_employees:
            emp_id, name, birth_date, gender, phone, email = emp
            
            # Áp dụng filter
            if filter_col == "Tất cả":
                search_in = f"{emp_id} {name} {gender} {phone} {email}".lower()
            elif filter_col == "ID":
                search_in = emp_id.lower()
            elif filter_col == "Họ và tên":
                search_in = name.lower()
            elif filter_col == "Giới tính":
                search_in = gender.lower()
            elif filter_col == "SDT":
                search_in = phone.lower()
            elif filter_col == "Email":
                search_in = email.lower()
            else:
                search_in = ""
            
            # Kiểm tra search text
            if not search_text or search_text in search_in:
                filtered_employees.append(emp)
        
        # Hiển thị kết quả
        for idx, emp in enumerate(filtered_employees, start=1):
            emp_id, name, birth_date, gender, phone, email = emp
            self.tree.insert(
                "",
                "end",
                values=(idx, emp_id, name, birth_date, gender, phone, email, "👁️ Xem | ✏️ Sửa | 🗑️ Xóa"),
                tags=("data",)
            )
        
        # Alternating colors
        for idx, item in enumerate(self.tree.get_children()):
            if idx % 2 == 1:
                self.tree.item(item, tags=("oddrow",))
        self.tree.tag_configure("oddrow", background="#F0F0F0")
    
    # ==================== EVENT HANDLERS ====================
    
    def on_row_double_click(self, event):
        """Xử lý khi double-click vào một dòng."""
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0], "values")
            employee_id = item_values[1]  # Cột ID
            self.show_employee_detail(employee_id)
    
    def show_employee_detail(self, employee_id):
        """Hiển thị chi tiết nhân viên."""
        self.detail_popup.show_employee_detail(employee_id)
    
    def show_add_employee_form(self):
        """Hiển thị form thêm nhân viên mới."""
        self.forms.show_add_employee_form(self.save_new_employee)
    
    def delete_selected_employee(self):
        """Xóa nhân viên đã chọn."""
        selected_item = self.tree.selection()
        if not selected_item:
            self.dialogs.show_warning_popup("Vui lòng chọn nhân viên cần xóa!")
            return
        
        item_values = self.tree.item(selected_item[0], "values")
        employee_id = item_values[1]  # Cột ID
        employee_name = item_values[2]  # Cột Họ và tên
        
        # Hiển thị popup xác nhận
        self.dialogs.show_confirm_delete_popup(
            employee_name,
            lambda popup: self.confirm_delete_employee(employee_id, popup)
        )
    
    def confirm_delete_employee(self, employee_id, popup):
        """Xác nhận xóa nhân viên."""
        # TODO: Gọi API để xóa
        # success = self.controller.delete_employee(employee_id)
        # if success:
        #     popup.destroy()
        #     self.dialogs.show_warning_popup("Xóa nhân viên thành công!")
        #     self.load_employees()
        # else:
        #     popup.destroy()
        #     self.dialogs.show_warning_popup("Xóa nhân viên thất bại!")
        
        # Giả lập xóa thành công
        popup.destroy()
        self.dialogs.show_warning_popup("Xóa nhân viên thành công!")
        self.load_employees()
    
    # ==================== SAVE NEW EMPLOYEE ====================
    
    def save_new_employee(self, employee_data, popup):
        """Lưu nhân viên mới.
        
        Args:
            employee_data (dict): Dữ liệu nhân viên đã validate
            popup: Popup form để đóng sau khi lưu thành công
        """
        # TODO: Gọi API để tạo nhân viên mới
        # success = self.controller.create_employee(employee_data)
        # if success:
        #     popup.destroy()
        #     self.dialogs.show_warning_popup("Thêm nhân viên thành công!")
        #     self.load_employees()
        # else:
        #     self.dialogs.show_warning_popup("Thêm nhân viên thất bại!")
        
        # Giả lập thêm thành công
        popup.destroy()
        self.dialogs.show_warning_popup("Thêm nhân viên thành công!")
        self.load_employees()
