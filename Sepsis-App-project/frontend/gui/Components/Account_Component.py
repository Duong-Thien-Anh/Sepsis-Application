import customtkinter as ctk
from tkinter import ttk
from controllers.Account_Controller import AccountController
from gui.Components.Account_Detail_Component import AccountDetail
from gui.Components.Account_Forms_Component import AccountForms
from gui.Components.Account_Dialogs_Component import AccountDialogs

class Account_UI(ctk.CTkFrame):
    """Giao diện quản lý tài khoản."""
    
    def __init__(self, master, controller=None):
        super().__init__(master, fg_color="transparent")
        
        self.controller = AccountController()
        
        # Khởi tạo các component con
        self.detail_popup = AccountDetail(self)
        self.forms = AccountForms(self)
        self.dialogs = AccountDialogs(self)
        
        self.pack(fill="both", expand=True)
        
        # Tạo giao diện
        self.create_widgets()
        
        # Load dữ liệu ban đầu
        self.load_accounts()
    
    # ==================== CREATE WIDGETS ====================
    
    def create_widgets(self):
        """Tạo các widget cho giao diện."""
        
        # ========== HEADER ==========
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="QUẢN LÝ TÀI KHOẢN",
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
            values=["Tất cả", "ID", "Tên đăng nhập", "Họ và tên", "Email", "Vai trò", "Trạng thái"],
            width=150,
            command=self.on_filter_change
        )
        self.filter_column.set("Tất cả")
        self.filter_column.pack(side="left", padx=(0, 20))
        
        # Entry tìm kiếm
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Tìm kiếm tài khoản...",
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
            command=self.search_accounts
        )
        search_button.pack(side="left", padx=(0, 10))
        
        # Nút Làm mới
        refresh_button = ctk.CTkButton(
            search_frame,
            text="Làm mới",
            width=100,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self.load_accounts
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
        columns = ("STT", "ID", "Tên đăng nhập", "Họ và tên", "Email", "Vai trò", "Trạng thái", "Tác vụ")
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
            "Tên đăng nhập": 150,
            "Họ và tên": 180,
            "Email": 200,
            "Vai trò": 120,
            "Trạng thái": 100,
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
        
        # Nút Thêm tài khoản
        add_button = ctk.CTkButton(
            button_frame,
            text="➕ Thêm tài khoản mới",
            width=180,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_add_account_form
        )
        add_button.pack(side="left", padx=(0, 10))
        
        # Nút Xóa tài khoản đã chọn
        delete_button = ctk.CTkButton(
            button_frame,
            text="🗑️ Xóa tài khoản",
            width=150,
            height=40,
            fg_color="#F44336",
            hover_color="#da190b",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.delete_selected_account
        )
        delete_button.pack(side="left")
    
    # ==================== LOAD DATA ====================
    
    def load_accounts(self):
        """Load danh sách tài khoản từ database."""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # TODO: Lấy dữ liệu từ API
        # accounts = self.controller.get_all_accounts()
        
        # Giả lập dữ liệu mẫu
        sample_accounts = [
            ("ACC001", "admin", "Quản trị viên", "admin@example.com", "Admin", "Hoạt động"),
            ("ACC002", "doctor01", "Bác sĩ Nguyễn Văn A", "doctor01@example.com", "Bác sĩ", "Hoạt động"),
            ("ACC003", "nurse01", "Y tá Trần Thị B", "nurse01@example.com", "Y tá", "Hoạt động"),
            ("ACC004", "staff01", "Nhân viên Lê Văn C", "staff01@example.com", "Nhân viên", "Tạm khóa"),
            ("ACC005", "user01", "Người dùng D", "user01@example.com", "Người dùng", "Hoạt động"),
        ]
        
        for idx, acc in enumerate(sample_accounts, start=1):
            acc_id, username, full_name, email, role, status = acc
            self.tree.insert(
                "",
                "end",
                values=(idx, acc_id, username, full_name, email, role, status, "👁️ Xem | ✏️ Sửa | 🗑️ Xóa"),
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
        self.search_accounts()
    
    def on_search(self, event):
        """Xử lý khi gõ vào ô tìm kiếm."""
        self.search_accounts()
    
    def search_accounts(self):
        """Tìm kiếm và lọc tài khoản."""
        search_text = self.search_entry.get().strip().lower()
        filter_col = self.filter_column.get()
        
        # Xóa dữ liệu hiện tại
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # TODO: Gọi API với filter và search
        # accounts = self.controller.search_accounts(search_text, filter_col)
        
        # Giả lập tìm kiếm trên dữ liệu mẫu
        sample_accounts = [
            ("ACC001", "admin", "Quản trị viên", "admin@example.com", "Admin", "Hoạt động"),
            ("ACC002", "doctor01", "Bác sĩ Nguyễn Văn A", "doctor01@example.com", "Bác sĩ", "Hoạt động"),
            ("ACC003", "nurse01", "Y tá Trần Thị B", "nurse01@example.com", "Y tá", "Hoạt động"),
            ("ACC004", "staff01", "Nhân viên Lê Văn C", "staff01@example.com", "Nhân viên", "Tạm khóa"),
            ("ACC005", "user01", "Người dùng D", "user01@example.com", "Người dùng", "Hoạt động"),
        ]
        
        filtered_accounts = []
        for acc in sample_accounts:
            acc_id, username, full_name, email, role, status = acc
            
            # Áp dụng filter
            if filter_col == "Tất cả":
                search_in = f"{acc_id} {username} {full_name} {email} {role} {status}".lower()
            elif filter_col == "ID":
                search_in = acc_id.lower()
            elif filter_col == "Tên đăng nhập":
                search_in = username.lower()
            elif filter_col == "Họ và tên":
                search_in = full_name.lower()
            elif filter_col == "Email":
                search_in = email.lower()
            elif filter_col == "Vai trò":
                search_in = role.lower()
            elif filter_col == "Trạng thái":
                search_in = status.lower()
            else:
                search_in = ""
            
            # Kiểm tra search text
            if not search_text or search_text in search_in:
                filtered_accounts.append(acc)
        
        # Hiển thị kết quả
        for idx, acc in enumerate(filtered_accounts, start=1):
            acc_id, username, full_name, email, role, status = acc
            self.tree.insert(
                "",
                "end",
                values=(idx, acc_id, username, full_name, email, role, status, "👁️ Xem | ✏️ Sửa | 🗑️ Xóa"),
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
            account_id = item_values[1]  # Cột ID
            self.show_account_detail(account_id)
    
    def show_account_detail(self, account_id):
        """Hiển thị chi tiết tài khoản."""
        self.detail_popup.show_account_detail(account_id)
    
    def show_add_account_form(self):
        """Hiển thị form thêm tài khoản mới."""
        self.forms.show_add_account_form(self.save_new_account)
    
    def delete_selected_account(self):
        """Xóa tài khoản đã chọn."""
        selected_item = self.tree.selection()
        if not selected_item:
            self.dialogs.show_warning_popup("Vui lòng chọn tài khoản cần xóa!")
            return
        
        item_values = self.tree.item(selected_item[0], "values")
        account_id = item_values[1]  # Cột ID
        account_name = item_values[3]  # Cột Họ và tên
        
        # Hiển thị popup xác nhận
        self.dialogs.show_confirm_delete_popup(
            account_name,
            lambda popup: self.confirm_delete_account(account_id, popup)
        )
    
    def confirm_delete_account(self, account_id, popup):
        """Xác nhận xóa tài khoản."""
        # TODO: Gọi API để xóa
        # success = self.controller.delete_account(account_id)
        # if success:
        #     popup.destroy()
        #     self.dialogs.show_warning_popup("Xóa tài khoản thành công!")
        #     self.load_accounts()
        # else:
        #     popup.destroy()
        #     self.dialogs.show_warning_popup("Xóa tài khoản thất bại!")
        
        # Giả lập xóa thành công
        popup.destroy()
        self.dialogs.show_warning_popup("Xóa tài khoản thành công!")
        self.load_accounts()
    
    # ==================== SAVE NEW ACCOUNT ====================
    
    def save_new_account(self, account_data, popup):
        """Lưu tài khoản mới.
        
        Args:
            account_data (dict): Dữ liệu tài khoản đã validate
            popup: Popup form để đóng sau khi lưu thành công
        """
        # TODO: Gọi API để tạo tài khoản mới
        # success = self.controller.create_account(account_data)
        # if success:
        #     popup.destroy()
        #     self.dialogs.show_warning_popup("Thêm tài khoản thành công!")
        #     self.load_accounts()
        # else:
        #     self.dialogs.show_warning_popup("Thêm tài khoản thất bại!")
        
        # Giả lập thêm thành công
        popup.destroy()
        self.dialogs.show_warning_popup("Thêm tài khoản thành công!")
        self.load_accounts()
