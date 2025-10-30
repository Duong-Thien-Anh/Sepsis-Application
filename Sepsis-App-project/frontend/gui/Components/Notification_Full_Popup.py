import customtkinter as ctk
from tkinter import messagebox

class NotificationFullPopup:
    """Popup hiển thị toàn bộ thông báo với chức năng quản lý."""
    
    def __init__(self, parent, controller):
        """
        Args:
            parent: Widget cha
            controller: NotificationController instance
        """
        self.parent = parent
        self.controller = controller
        self.popup = None
        self.notification_list_frame = None
    
    def show(self):
        """Hiển thị popup."""
        # Tạo popup window
        self.popup = ctk.CTkToplevel(self.parent)
        self.popup.title("Quản lý thông báo")
        self.popup.geometry("900x700")
        
        # Center popup
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.popup.winfo_screenheight() // 2) - (700 // 2)
        self.popup.geometry(f"900x700+{x}+{y}")
        
        # Main container
        main_container = ctk.CTkFrame(self.popup, fg_color="white")
        main_container.pack(fill="both", expand=True)
        
        # ========== HEADER ==========
        self.create_header(main_container)
        
        # ========== FILTER BUTTONS ==========
        self.create_filter_buttons(main_container)
        
        # ========== NOTIFICATION LIST ==========
        self.create_notification_list(main_container)
        
        # ========== FOOTER ==========
        self.create_footer(main_container)
        
        # Focus popup
        self.popup.focus_force()
    
    def create_header(self, parent):
        """Tạo header của popup."""
        header_frame = ctk.CTkFrame(parent, fg_color="#66B7FF", height=70)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔔 Quản lý thông báo",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Badge số lượng chưa đọc
        unread_count = self.controller.get_unread_count()
        if unread_count > 0:
            badge = ctk.CTkLabel(
                header_frame,
                text=f"{unread_count} chưa đọc",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#66B7FF",
                fg_color="white",
                corner_radius=15,
                width=80,
                height=30
            )
            badge.pack(side="left", padx=5, pady=15)
        
        # Nút đóng
        close_btn = ctk.CTkButton(
            header_frame,
            text="✕",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="white",
            text_color="#66B7FF",
            hover_color="#FFE5E5",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self.popup.destroy
        )
        close_btn.pack(side="right", padx=20, pady=15)
    
    def create_filter_buttons(self, parent):
        """Tạo các nút filter."""
        filter_frame = ctk.CTkFrame(parent, fg_color="white", height=60)
        filter_frame.pack(fill="x", padx=20, pady=(15, 5))
        filter_frame.pack_propagate(False)
        
        # Label
        filter_label = ctk.CTkLabel(
            filter_frame,
            text="Lọc:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="black"
        )
        filter_label.pack(side="left", padx=(10, 15))
        
        # Buttons
        filters = [
            ('Tất cả', 'all'),
            ('Chưa đọc', 'unread'),
            ('Đã đọc', 'read')
        ]
        
        for text, filter_type in filters:
            is_active = self.controller.get_current_filter() == filter_type
            
            fg_col = "#66B7FF" if is_active else "white"
            txt_col = "white" if is_active else "#66B7FF"
            hov_col = "#5aa3e0" if is_active else "#E3F2FD"
            
            btn = ctk.CTkButton(
                filter_frame,
                text=text,
                width=100,
                height=35,
                corner_radius=8,
                fg_color=fg_col,
                text_color=txt_col,
                border_width=2,
                border_color="#66B7FF",
                hover_color=hov_col,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda f=filter_type: self.on_filter_change(f)
            )
            btn.pack(side="left", padx=5)
        
        # Nút đánh dấu tất cả đã đọc
        mark_all_btn = ctk.CTkButton(
            filter_frame,
            text="✓ Đọc tất cả",
            width=120,
            height=35,
            corner_radius=8,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.on_mark_all_read
        )
        mark_all_btn.pack(side="right", padx=5)
    
    def create_notification_list(self, parent):
        """Tạo danh sách thông báo."""
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(
            parent,
            fg_color="#F7F7F5",
            scrollbar_button_color="#66B7FF",
            scrollbar_button_hover_color="#5aa3e0",
            corner_radius=10
        )
        scrollable.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.notification_list_frame = scrollable
        
        # Hiển thị thông báo
        self.display_notifications()
    
    def display_notifications(self):
        """Hiển thị danh sách thông báo theo filter."""
        # Xóa nội dung cũ
        for widget in self.notification_list_frame.winfo_children():
            widget.destroy()
        
        # Lấy thông báo theo filter
        notifications = self.controller.get_filtered_notifications()
        
        if not notifications:
            # Không có thông báo
            empty_label = ctk.CTkLabel(
                self.notification_list_frame,
                text="📭 Không có thông báo nào",
                font=ctk.CTkFont(size=16),
                text_color="#757575"
            )
            empty_label.pack(pady=50)
            return
        
        # Hiển thị từng thông báo
        for notif in notifications:
            self.create_notification_card(self.notification_list_frame, notif)
    
    def create_notification_card(self, parent, notification):
        """Tạo card thông báo."""
        # Màu nền theo trạng thái
        bg_color = "white" if notification['read'] else "#E3F2FD"
        border_color = self.controller.get_notification_color(notification['type'])
        
        # Card frame
        card = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=10,
            border_width=2,
            border_color=border_color
        )
        card.pack(fill="x", pady=8, padx=10)
        
        # Left - Icon
        icon_frame = ctk.CTkFrame(card, fg_color="transparent", width=60)
        icon_frame.grid(row=0, column=0, rowspan=3, padx=15, pady=15, sticky="n")
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=self.controller.get_notification_icon(notification['type']),
            font=ctk.CTkFont(size=30)
        )
        icon_label.pack()
        
        # Middle - Content
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=notification['title'],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="black",
            anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="ew", padx=10, pady=(15, 5))
        
        # Message
        message_label = ctk.CTkLabel(
            card,
            text=notification['message'],
            font=ctk.CTkFont(size=13),
            text_color="#5D5C5C",
            anchor="w",
            wraplength=550,
            justify="left"
        )
        message_label.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Time
        time_label = ctk.CTkLabel(
            card,
            text=f"🕐 {notification['time']}",
            font=ctk.CTkFont(size=11),
            text_color="#9E9E9E",
            anchor="w"
        )
        time_label.grid(row=2, column=1, sticky="w", padx=10, pady=(5, 15))
        
        # Right - Action buttons
        action_frame = ctk.CTkFrame(card, fg_color="transparent", width=150)
        action_frame.grid(row=0, column=2, rowspan=3, padx=15, pady=15)
        
        # Nút toggle đọc/chưa đọc
        read_btn_text = "Đánh dấu chưa đọc" if notification['read'] else "Đánh dấu đã đọc"
        read_btn = ctk.CTkButton(
            action_frame,
            text=read_btn_text,
            width=130,
            height=30,
            corner_radius=8,
            fg_color="#2196F3",
            hover_color="#1976D2",
            font=ctk.CTkFont(size=11),
            command=lambda: self.on_toggle_read(notification['id'])
        )
        read_btn.pack(pady=5)
        
        # Nút xóa
        delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Xóa",
            width=130,
            height=30,
            corner_radius=8,
            fg_color="#F44336",
            hover_color="#D32F2F",
            font=ctk.CTkFont(size=11),
            command=lambda: self.on_delete(notification['id'])
        )
        delete_btn.pack(pady=5)
        
        # Configure grid
        card.grid_columnconfigure(1, weight=1)
    
    def create_footer(self, parent):
        """Tạo footer với nút xóa tất cả."""
        footer_frame = ctk.CTkFrame(parent, fg_color="white", height=60)
        footer_frame.pack(fill="x", padx=20, pady=(5, 15))
        footer_frame.pack_propagate(False)
        
        # Nút xóa tất cả
        delete_all_btn = ctk.CTkButton(
            footer_frame,
            text="🗑️ Xóa tất cả thông báo",
            width=200,
            height=40,
            corner_radius=8,
            fg_color="#F44336",
            hover_color="#D32F2F",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_delete_all
        )
        delete_all_btn.pack(side="left", padx=10, pady=10)
        
        # Tổng số thông báo
        total = len(self.controller.get_all_notifications())
        unread = self.controller.get_unread_count()
        
        info_label = ctk.CTkLabel(
            footer_frame,
            text=f"Tổng: {total} thông báo | {unread} chưa đọc",
            font=ctk.CTkFont(size=12),
            text_color="#757575"
        )
        info_label.pack(side="right", padx=20, pady=10)
    
    # ==================== EVENT HANDLERS ====================
    
    def on_filter_change(self, filter_type):
        """Xử lý thay đổi filter."""
        self.controller.set_filter(filter_type)
        self.refresh()
    
    def on_mark_all_read(self):
        """Xử lý đánh dấu tất cả đã đọc."""
        self.controller.mark_all_as_read()
        self.refresh()
    
    def on_toggle_read(self, notification_id):
        """Xử lý toggle trạng thái đọc."""
        self.controller.toggle_read_status(notification_id)
        self.refresh()
    
    def on_delete(self, notification_id):
        """Xử lý xóa thông báo."""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa thông báo này?", parent=self.popup):
            self.controller.delete_notification(notification_id)
            self.refresh()
    
    def on_delete_all(self):
        """Xử lý xóa tất cả thông báo."""
        if messagebox.askyesno(
            "Xác nhận", 
            "Bạn có chắc muốn xóa TẤT CẢ thông báo?\nHành động này không thể hoàn tác!", 
            parent=self.popup
        ):
            self.controller.delete_all_notifications()
            self.refresh()
    
    def refresh(self):
        """Làm mới giao diện."""
        # Destroy và tạo lại popup
        self.popup.destroy()
        self.show()
