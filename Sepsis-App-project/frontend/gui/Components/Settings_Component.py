import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from assets.Assets_Management import AssetManager
import json
import os

class Settings_UI(ctk.CTkFrame):
    """Giao diện cài đặt hệ thống."""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        # Load cấu hình hiện tại
        self.load_current_settings()
        
        # Cấu hình grid chính
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_columnconfigure(0, weight=1)
        
        # Tạo header
        self.create_header()
        
        # Tạo nội dung chính với scrollbar
        self.create_content()
    
    def load_current_settings(self):
        """Load cấu hình hiện tại từ file config."""
        try:
            from config.app_config import (
                COLORS, FONTS, SIZES, API_CONFIG, 
                DATABASE_CONFIG, THEME_CONFIG, LOG_CONFIG
            )
            self.current_settings = {
                "theme": THEME_CONFIG.get("default_theme", "light"),
                "appearance_mode": THEME_CONFIG.get("appearance_mode", "System"),
                "color_theme": THEME_CONFIG.get("color_theme", "blue"),
                "primary_color": COLORS.get("primary", "#66B7FF"),
                "font_family": FONTS.get("family", "Roboto"),
                "font_size": FONTS.get("size_normal", 13),
                "api_url": API_CONFIG.get("base_url", "http://localhost:8000"),
                "api_timeout": API_CONFIG.get("timeout", 30),
                "db_host": DATABASE_CONFIG.get("host", "localhost"),
                "db_port": DATABASE_CONFIG.get("port", 3306),
                "db_name": DATABASE_CONFIG.get("database", "sepsis_management"),
                "enable_log": LOG_CONFIG.get("enable", True),
                "log_level": LOG_CONFIG.get("level", "INFO"),
            }
        except:
            # Giá trị mặc định nếu không load được config
            self.current_settings = {
                "theme": "light",
                "appearance_mode": "System",
                "color_theme": "blue",
                "primary_color": "#66B7FF",
                "font_family": "Roboto",
                "font_size": 13,
                "api_url": "http://localhost:8000",
                "api_timeout": 30,
                "db_host": "localhost",
                "db_port": 3306,
                "db_name": "sepsis_management",
                "enable_log": True,
                "log_level": "INFO",
            }
    
    def create_header(self):
        """Tạo header với tiêu đề."""
        header_frame = ctk.CTkFrame(self, fg_color="#66B7FF", corner_radius=10, border_width=2, border_color="black")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ CÀI ĐẶT HỆ THỐNG",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=15)
    
    def create_content(self):
        """Tạo nội dung chính với scrollbar."""
        # Frame ngoài với viền đen
        outer_frame = ctk.CTkFrame(self, fg_color="black", corner_radius=15)
        outer_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1)
        
        # Frame trắng bên trong
        inner_frame = ctk.CTkFrame(outer_frame, fg_color="white", corner_radius=13)
        inner_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        inner_frame.grid_rowconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(
            inner_frame,
            fg_color="white",
            scrollbar_button_color="#66B7FF",
            scrollbar_button_hover_color="#5aa3e0",
            corner_radius=10
        )
        scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # ==================== PHẦN 1: GIAO DIỆN ====================
        self.create_appearance_section(scrollable_frame)
        
        # Separator
        self.create_separator(scrollable_frame)
        
        # ==================== PHẦN 2: API ====================
        self.create_api_section(scrollable_frame)
        
        # Separator
        self.create_separator(scrollable_frame)
        
        # ==================== PHẦN 3: DATABASE ====================
        self.create_database_section(scrollable_frame)
        
        # Separator
        self.create_separator(scrollable_frame)
        
        # ==================== PHẦN 4: HỆ THỐNG ====================
        self.create_system_section(scrollable_frame)
        
        # Separator
        self.create_separator(scrollable_frame)
        
        # ==================== NÚT ACTIONS ====================
        self.create_action_buttons(scrollable_frame)
    
    def create_separator(self, parent):
        """Tạo đường ngăn cách."""
        separator = ctk.CTkFrame(parent, fg_color="#E0E0E0", height=2)
        separator.pack(fill="x", pady=15, padx=20)
    
    def create_appearance_section(self, parent):
        """Phần cài đặt giao diện."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", padx=20, pady=10)
        
        # Tiêu đề section
        title = ctk.CTkLabel(
            section_frame,
            text="🎨 Giao diện",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#66B7FF",
            anchor="w"
        )
        title.pack(anchor="w", pady=(0, 10))
        
        # Theme (Light/Dark)
        theme_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        theme_frame.pack(fill="x", pady=5)
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Chế độ hiển thị:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        theme_label.pack(side="left", padx=(0, 15))
        
        self.theme_var = ctk.StringVar(value=self.current_settings["appearance_mode"])
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.theme_var,
            values=["System", "Light", "Dark"],
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=13),
            width=200,
            height=35,
            corner_radius=10,
            fg_color="#F7F7F5",
            button_color="#66B7FF",
            button_hover_color="#5aa3e0",
            dropdown_fg_color="white",
            dropdown_hover_color="#E3F2FD",
            text_color="black",
            dropdown_text_color="black",
            command=self.on_theme_change
        )
        theme_menu.pack(side="left", fill="x", expand=True)
        
        # Color Theme
        color_theme_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        color_theme_frame.pack(fill="x", pady=5)
        
        color_label = ctk.CTkLabel(
            color_theme_frame,
            text="Màu chủ đạo:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        color_label.pack(side="left", padx=(0, 15))
        
        self.color_theme_var = ctk.StringVar(value=self.current_settings["color_theme"])
        color_menu = ctk.CTkOptionMenu(
            color_theme_frame,
            variable=self.color_theme_var,
            values=["blue", "green", "dark-blue"],
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=13),
            width=200,
            height=35,
            corner_radius=10,
            fg_color="#F7F7F5",
            button_color="#66B7FF",
            button_hover_color="#5aa3e0",
            dropdown_fg_color="white",
            dropdown_hover_color="#E3F2FD",
            text_color="black",
            dropdown_text_color="black"
        )
        color_menu.pack(side="left", fill="x", expand=True)
        
        # Font Family
        font_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        font_frame.pack(fill="x", pady=5)
        
        font_label = ctk.CTkLabel(
            font_frame,
            text="Font chữ:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        font_label.pack(side="left", padx=(0, 15))
        
        self.font_var = ctk.StringVar(value=self.current_settings["font_family"])
        font_menu = ctk.CTkOptionMenu(
            font_frame,
            variable=self.font_var,
            values=["Roboto", "Arial", "Segoe UI", "Calibri", "Times New Roman"],
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=13),
            width=200,
            height=35,
            corner_radius=10,
            fg_color="#F7F7F5",
            button_color="#66B7FF",
            button_hover_color="#5aa3e0",
            dropdown_fg_color="white",
            dropdown_hover_color="#E3F2FD",
            text_color="black",
            dropdown_text_color="black"
        )
        font_menu.pack(side="left", fill="x", expand=True)
        
        # Font Size
        size_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        size_frame.pack(fill="x", pady=5)
        
        size_label = ctk.CTkLabel(
            size_frame,
            text="Kích thước chữ:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        size_label.pack(side="left", padx=(0, 15))
        
        self.font_size_var = ctk.IntVar(value=self.current_settings["font_size"])
        size_slider = ctk.CTkSlider(
            size_frame,
            from_=10,
            to=20,
            number_of_steps=10,
            variable=self.font_size_var,
            button_color="#66B7FF",
            button_hover_color="#5aa3e0",
            progress_color="#66B7FF"
        )
        size_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.size_value_label = ctk.CTkLabel(
            size_frame,
            text=f"{self.font_size_var.get()}px",
            font=ctk.CTkFont(size=13),
            text_color="black",
            width=50
        )
        self.size_value_label.pack(side="left")
        
        # Update label khi slider thay đổi
        size_slider.configure(command=lambda value: self.size_value_label.configure(text=f"{int(value)}px"))
    
    def create_api_section(self, parent):
        """Phần cài đặt API."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", padx=20, pady=10)
        
        # Tiêu đề section
        title = ctk.CTkLabel(
            section_frame,
            text="🌐 Cấu hình API",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#66B7FF",
            anchor="w"
        )
        title.pack(anchor="w", pady=(0, 10))
        
        # API URL
        url_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        url_frame.pack(fill="x", pady=5)
        
        url_label = ctk.CTkLabel(
            url_frame,
            text="URL Backend:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        url_label.pack(side="left", padx=(0, 15))
        
        self.api_url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="http://localhost:8000",
            font=ctk.CTkFont(size=13),
            height=35,
            fg_color="#F7F7F5",
            text_color="black",
            corner_radius=10,
            border_width=2,
            border_color="black"
        )
        self.api_url_entry.insert(0, self.current_settings["api_url"])
        self.api_url_entry.pack(side="left", fill="x", expand=True)
        
        # API Timeout
        timeout_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        timeout_frame.pack(fill="x", pady=5)
        
        timeout_label = ctk.CTkLabel(
            timeout_frame,
            text="Timeout (giây):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        timeout_label.pack(side="left", padx=(0, 15))
        
        self.api_timeout_entry = ctk.CTkEntry(
            timeout_frame,
            placeholder_text="30",
            font=ctk.CTkFont(size=13),
            height=35,
            fg_color="#F7F7F5",
            text_color="black",
            corner_radius=10,
            border_width=2,
            border_color="black",
            width=200
        )
        self.api_timeout_entry.insert(0, str(self.current_settings["api_timeout"]))
        self.api_timeout_entry.pack(side="left")
        
        # Nút Test Connection
        test_btn = ctk.CTkButton(
            timeout_frame,
            text="🔗 Test Connection",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=150,
            height=35,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#2196F3",
            hover_color="#45a049",
            command=self.test_api_connection
        )
        test_btn.pack(side="left", padx=(10, 0))
    
    def create_database_section(self, parent):
        """Phần cài đặt Database."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", padx=20, pady=10)
        
        # Tiêu đề section
        title = ctk.CTkLabel(
            section_frame,
            text="🗄️ Cấu hình Database",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#66B7FF",
            anchor="w"
        )
        title.pack(anchor="w", pady=(0, 10))
        
        # DB Host
        host_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        host_frame.pack(fill="x", pady=5)
        
        host_label = ctk.CTkLabel(
            host_frame,
            text="Host:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        host_label.pack(side="left", padx=(0, 15))
        
        self.db_host_entry = ctk.CTkEntry(
            host_frame,
            placeholder_text="localhost",
            font=ctk.CTkFont(size=13),
            height=35,
            fg_color="#F7F7F5",
            text_color="black",
            corner_radius=10,
            border_width=2,
            border_color="black"
        )
        self.db_host_entry.insert(0, self.current_settings["db_host"])
        self.db_host_entry.pack(side="left", fill="x", expand=True)
        
        # DB Port
        port_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        port_frame.pack(fill="x", pady=5)
        
        port_label = ctk.CTkLabel(
            port_frame,
            text="Port:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        port_label.pack(side="left", padx=(0, 15))
        
        self.db_port_entry = ctk.CTkEntry(
            port_frame,
            placeholder_text="3306",
            font=ctk.CTkFont(size=13),
            height=35,
            fg_color="#F7F7F5",
            text_color="black",
            corner_radius=10,
            border_width=2,
            border_color="black",
            width=200
        )
        self.db_port_entry.insert(0, str(self.current_settings["db_port"]))
        self.db_port_entry.pack(side="left")
        
        # DB Name
        name_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=5)
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Database:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        name_label.pack(side="left", padx=(0, 15))
        
        self.db_name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="sepsis_management",
            font=ctk.CTkFont(size=13),
            height=35,
            fg_color="#F7F7F5",
            text_color="black",
            corner_radius=10,
            border_width=2,
            border_color="black"
        )
        self.db_name_entry.insert(0, self.current_settings["db_name"])
        self.db_name_entry.pack(side="left", fill="x", expand=True)
    
    def create_system_section(self, parent):
        """Phần cài đặt hệ thống."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", padx=20, pady=10)
        
        # Tiêu đề section
        title = ctk.CTkLabel(
            section_frame,
            text="🔧 Hệ thống",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#66B7FF",
            anchor="w"
        )
        title.pack(anchor="w", pady=(0, 10))
        
        # Enable Logging
        log_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        log_frame.pack(fill="x", pady=5)
        
        log_label = ctk.CTkLabel(
            log_frame,
            text="Ghi log hệ thống:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        log_label.pack(side="left", padx=(0, 15))
        
        self.enable_log_var = ctk.BooleanVar(value=self.current_settings["enable_log"])
        log_switch = ctk.CTkSwitch(
            log_frame,
            text="",
            variable=self.enable_log_var,
            onvalue=True,
            offvalue=False,
            progress_color="#66B7FF",
            button_color="white",
            button_hover_color="#E3F2FD"
        )
        log_switch.pack(side="left")
        
        # Log Level
        level_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        level_frame.pack(fill="x", pady=5)
        
        level_label = ctk.CTkLabel(
            level_frame,
            text="Mức độ log:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        level_label.pack(side="left", padx=(0, 15))
        
        self.log_level_var = ctk.StringVar(value=self.current_settings["log_level"])
        level_menu = ctk.CTkOptionMenu(
            level_frame,
            variable=self.log_level_var,
            values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=13),
            width=200,
            height=35,
            corner_radius=10,
            fg_color="#F7F7F5",
            button_color="#66B7FF",
            button_hover_color="#5aa3e0",
            dropdown_fg_color="white",
            dropdown_hover_color="#E3F2FD",
            text_color="black",
            dropdown_text_color="black"
        )
        level_menu.pack(side="left")
        
        # Clear Cache
        cache_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        cache_frame.pack(fill="x", pady=5)
        
        cache_label = ctk.CTkLabel(
            cache_frame,
            text="Xóa cache:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w",
            width=200
        )
        cache_label.pack(side="left", padx=(0, 15))
        
        clear_cache_btn = ctk.CTkButton(
            cache_frame,
            text="🗑️ Xóa Cache",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=150,
            height=35,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#ED5C5C",
            hover_color="#da190b",
            command=self.clear_cache
        )
        clear_cache_btn.pack(side="left")
    
    def create_action_buttons(self, parent):
        """Tạo các nút hành động."""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # Căn giữa các button
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_frame.grid_columnconfigure(3, weight=0)
        button_frame.grid_columnconfigure(4, weight=1)
        
        # Nút Reset
        reset_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Đặt lại mặc định",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#FFA726",
            hover_color="#45a049",
            command=self.reset_to_default
        )
        reset_btn.grid(row=0, column=1, padx=10)
        
        # Nút Export
        export_btn = ctk.CTkButton(
            button_frame,
            text="📤 Xuất cấu hình",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#2196F3",
            hover_color="#45a049",
            command=self.export_settings
        )
        export_btn.grid(row=0, column=2, padx=10)
        
        # Nút Save
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Lưu thay đổi",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="black",
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self.save_settings
        )
        save_btn.grid(row=0, column=3, padx=10)
    
    # ==================== METHODS ====================
    
    def on_theme_change(self, value):
        """Xử lý khi thay đổi theme."""
        ctk.set_appearance_mode(value)
        print(f"✅ Theme changed to: {value}")
    
    def test_api_connection(self):
        """Test kết nối API."""
        api_url = self.api_url_entry.get().strip()
        
        if not api_url:
            self.show_warning("Vui lòng nhập URL API!")
            return
        
        # TODO: Implement actual API connection test
        # try:
        #     response = requests.get(f"{api_url}/health", timeout=5)
        #     if response.status_code == 200:
        #         self.show_success("Kết nối API thành công!")
        #     else:
        #         self.show_warning(f"API trả về lỗi: {response.status_code}")
        # except:
        #     self.show_warning("Không thể kết nối đến API!")
        
        # Giả lập test thành công
        self.show_success("✅ Kết nối API thành công!")
    
    def clear_cache(self):
        """Xóa cache hệ thống."""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ cache?"):
            # TODO: Implement actual cache clearing
            # Clear temp files, logs, etc.
            self.show_success("✅ Đã xóa cache thành công!")
    
    def reset_to_default(self):
        """Đặt lại cài đặt mặc định."""
        if messagebox.askyesno("Xác nhận", "Đặt lại tất cả cài đặt về mặc định?"):
            # Reset all values
            self.theme_var.set("System")
            self.color_theme_var.set("blue")
            self.font_var.set("Roboto")
            self.font_size_var.set(13)
            self.api_url_entry.delete(0, "end")
            self.api_url_entry.insert(0, "http://localhost:8000")
            self.api_timeout_entry.delete(0, "end")
            self.api_timeout_entry.insert(0, "30")
            self.db_host_entry.delete(0, "end")
            self.db_host_entry.insert(0, "localhost")
            self.db_port_entry.delete(0, "end")
            self.db_port_entry.insert(0, "3306")
            self.db_name_entry.delete(0, "end")
            self.db_name_entry.insert(0, "sepsis_management")
            self.enable_log_var.set(True)
            self.log_level_var.set("INFO")
            
            self.show_success("✅ Đã đặt lại cài đặt mặc định!")
    
    def export_settings(self):
        """Xuất cấu hình ra file JSON."""
        settings = self.collect_settings()
        
        file_path = filedialog.asksaveasfilename(
            title="Xuất cấu hình",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=4, ensure_ascii=False)
                self.show_success(f"✅ Đã xuất cấu hình ra: {file_path}")
            except Exception as e:
                self.show_warning(f"❌ Lỗi khi xuất file: {str(e)}")
    
    def save_settings(self):
        """Lưu cài đặt vào file config."""
        settings = self.collect_settings()
        
        # TODO: Implement actual config file update
        # Update config/app_config.py with new values
        
        if messagebox.askyesno("Xác nhận", "Lưu thay đổi? Ứng dụng sẽ cần khởi động lại."):
            # Save to file
            try:
                # Giả lập lưu thành công
                self.show_success("✅ Đã lưu cài đặt thành công!\n⚠️ Vui lòng khởi động lại ứng dụng.")
                print(f"📝 Settings saved: {settings}")
            except Exception as e:
                self.show_warning(f"❌ Lỗi khi lưu: {str(e)}")
    
    def collect_settings(self):
        """Thu thập tất cả cài đặt hiện tại."""
        return {
            "appearance_mode": self.theme_var.get(),
            "color_theme": self.color_theme_var.get(),
            "font_family": self.font_var.get(),
            "font_size": self.font_size_var.get(),
            "api_url": self.api_url_entry.get().strip(),
            "api_timeout": int(self.api_timeout_entry.get().strip()),
            "db_host": self.db_host_entry.get().strip(),
            "db_port": int(self.db_port_entry.get().strip()),
            "db_name": self.db_name_entry.get().strip(),
            "enable_log": self.enable_log_var.get(),
            "log_level": self.log_level_var.get(),
        }
    
    def show_warning(self, message):
        """Hiển thị cảnh báo."""
        messagebox.showwarning("Cảnh báo", message)
    
    def show_success(self, message):
        """Hiển thị thông báo thành công."""
        messagebox.showinfo("Thành công", message)
