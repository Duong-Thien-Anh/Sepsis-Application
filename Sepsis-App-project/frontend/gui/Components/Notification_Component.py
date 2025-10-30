import customtkinter as ctk
from PIL import Image
from assets.Assets_Management import AssetManager
from controllers.Notification_Controller import NotificationController

class NotificationUI:
    """Component UI cho hệ thống thông báo."""
    
    def __init__(self, parent):
        """
        Args:
            parent: Widget cha (Header Component)
        """
        self.parent = parent
        self.controller = NotificationController()
        
        # Reference đến dropdown và popup
        self.dropdown = None
        
        # Biến theo dõi click
        self.click_count = 0
        self.click_timer = None
    
    def create_notification_button(self, parent_frame):
        """
        Tạo button thông báo với badge.
        
        Args:
            parent_frame: Frame cha để đặt button
            
        Returns:
            Frame chứa notification button
        """
        # ========== LOAD ICON ==========
        path_bell = AssetManager.get_icon_path("icon_Bell")
        bell_img = Image.open(path_bell).resize((30, 30))
        bell_ctk = ctk.CTkImage(bell_img)

        # ========== FRAME chứa ==========
        frame = ctk.CTkFrame(
            parent_frame, 
            fg_color="white", 
            width=50, 
            height=50, 
            corner_radius=30, 
            border_color="black", 
            border_width=2
        )
        frame.image_refs = (bell_ctk,)  # giữ reference

        # Chuông nằm giữa
        bell = ctk.CTkLabel(frame, image=bell_ctk, text="", fg_color="transparent")
        bell.place(relx=0.5, rely=0.5, anchor="center")

        # Badge đỏ (ảnh PNG) đặt ở góc phải trên
        badge_frame = ctk.CTkFrame(
            frame, 
            fg_color="red", 
            width=15, 
            height=15, 
            corner_radius=15, 
            border_color="black", 
            border_width=2
        )

        # ========== SETUP EVENTS ==========
        def on_notification_click(event):
            """Xử lý click vào notification button."""
            self.click_count += 1
            
            # Hủy timer cũ nếu có
            if self.click_timer:
                frame.after_cancel(self.click_timer)
            
            # Set timer để reset click count
            def reset_click():
                if self.click_count == 1:
                    # Single click - Toggle dropdown menu
                    self.toggle_dropdown(frame)
                elif self.click_count >= 2:
                    # Double click - Show full notification popup
                    self.show_full_popup()
                    # Đóng dropdown nếu đang mở
                    if self.dropdown and self.dropdown.winfo_exists():
                        self.dropdown.destroy()
                        self.dropdown = None
                
                self.click_count = 0
                self.click_timer = None
            
            self.click_timer = frame.after(300, reset_click)  # 300ms để phát hiện double-click
        
        # Hover effect
        def on_enter(e):
            frame.configure(fg_color="#FE5858")   # đỏ khi hover
        
        def on_leave(e):
            frame.configure(fg_color="white")     # trở về trắng

        # Bind events
        for widget in (frame, bell, badge_frame):
            widget.bind("<Enter>", on_enter)    
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_notification_click)

        # Hiển thị badge nếu có thông báo chưa đọc
        unread_count = self.controller.get_unread_count()
        if unread_count > 0:
            badge_frame.place(relx=0.75, rely=0.25, anchor="center")
            badge_frame.lift()
            
            # Hiển thị số lượng thông báo chưa đọc
            badge_label = ctk.CTkLabel(
                badge_frame,
                text=str(unread_count),
                font=ctk.CTkFont(size=8, weight="bold"),
                text_color="white",
                fg_color="transparent"
            )
            badge_label.place(relx=0.5, rely=0.5, anchor="center")

        frame.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        return frame
    
    # ==================== DROPDOWN MENU ====================
    
    def toggle_dropdown(self, parent_frame):
        """Toggle dropdown menu thông báo."""
        if self.dropdown and self.dropdown.winfo_exists():
            # Nếu đã mở thì đóng
            self.dropdown.destroy()
            self.dropdown = None
        else:
            # Tạo dropdown mới
            self.show_dropdown(parent_frame)
    
    def show_dropdown(self, parent_frame):
        """Hiển thị dropdown menu thông báo."""
        # Tạo toplevel window
        dropdown = ctk.CTkToplevel(self.parent)
        dropdown.withdraw()  # Ẩn trước
        dropdown.overrideredirect(True)  # Bỏ title bar
        
        # Lưu reference
        self.dropdown = dropdown
        
        # Main container
        container = ctk.CTkFrame(
            dropdown,
            fg_color="white",
            corner_radius=10,
            border_width=2,
            border_color="black",
            width=350,
            height=400
        )
        container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header
        header_frame = ctk.CTkFrame(container, fg_color="#66B7FF", corner_radius=8)
        header_frame.pack(fill="x", padx=8, pady=8)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="🔔 Thông báo",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        header_label.pack(side="left", padx=10, pady=8)
        
        # Nút đánh dấu đã đọc tất cả
        mark_all_btn = ctk.CTkButton(
            header_frame,
            text="Đọc tất cả",
            width=80,
            height=25,
            corner_radius=5,
            fg_color="white",
            text_color="#66B7FF",
            hover_color="#E3F2FD",
            font=ctk.CTkFont(size=11),
            command=lambda: self.on_mark_all_read(dropdown)
        )
        mark_all_btn.pack(side="right", padx=10, pady=8)
        
        # Scrollable frame cho danh sách thông báo
        scrollable = ctk.CTkScrollableFrame(
            container,
            fg_color="white",
            scrollbar_button_color="#66B7FF",
            scrollbar_button_hover_color="#5aa3e0",
            corner_radius=0
        )
        scrollable.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        # Hiển thị 3 thông báo gần nhất
        recent_notifications = self.controller.get_recent_notifications(limit=3)
        
        if recent_notifications:
            for notif in recent_notifications:
                self.create_dropdown_item(scrollable, notif)
        else:
            no_notif_label = ctk.CTkLabel(
                scrollable,
                text="📭 Không có thông báo nào",
                font=ctk.CTkFont(size=13),
                text_color="#757575"
            )
            no_notif_label.pack(pady=30)
        
        # Footer - Nút xem tất cả
        footer_frame = ctk.CTkFrame(container, fg_color="white", height=40)
        footer_frame.pack(fill="x", padx=8, pady=(0, 8))
        
        view_all_btn = ctk.CTkButton(
            footer_frame,
            text="Xem tất cả thông báo",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2196F3",
            hover_color="#45a049",
            corner_radius=8,
            height=35,
            command=lambda: [dropdown.destroy(), self.show_full_popup()]
        )
        view_all_btn.pack(fill="x", pady=5)
        
        # Tính toán vị trí hiển thị dropdown
        parent_frame.update_idletasks()
        x = parent_frame.winfo_rootx() - 300  # Hiển thị bên trái button
        y = parent_frame.winfo_rooty() + parent_frame.winfo_height() + 5  # Dưới button
        
        dropdown.geometry(f"350x400+{x}+{y}")
        dropdown.deiconify()  # Hiển thị
        dropdown.lift()
        dropdown.focus_force()
        
        # Đóng dropdown khi click ra ngoài
        dropdown.bind("<FocusOut>", lambda e: dropdown.after(100, lambda: dropdown.destroy() if dropdown.winfo_exists() else None))
    
    def create_dropdown_item(self, parent, notification):
        """Tạo item thông báo trong dropdown."""
        # Màu nền theo trạng thái đọc
        bg_color = "white" if notification['read'] else "#E3F2FD"
        
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0"
        )
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # Icon
        icon_label = ctk.CTkLabel(
            item_frame,
            text=self.controller.get_notification_icon(notification['type']),
            font=ctk.CTkFont(size=20)
        )
        icon_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="n")
        
        # Tiêu đề
        title_label = ctk.CTkLabel(
            item_frame,
            text=notification['title'],
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="black",
            anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=(10, 2))
        
        # Nội dung
        message_label = ctk.CTkLabel(
            item_frame,
            text=notification['message'],
            font=ctk.CTkFont(size=11),
            text_color="#5D5C5C",
            anchor="w",
            wraplength=250,
            justify="left"
        )
        message_label.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 5))
        
        # Thời gian
        time_label = ctk.CTkLabel(
            item_frame,
            text=notification['time'],
            font=ctk.CTkFont(size=10),
            text_color="#9E9E9E",
            anchor="w"
        )
        time_label.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=(0, 10))
        
        # Cấu hình grid
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Click để đánh dấu đã đọc
        def mark_as_read(e):
            self.controller.mark_as_read(notification['id'])
            item_frame.configure(fg_color="white")
        
        item_frame.bind("<Button-1>", mark_as_read)
        for widget in [icon_label, title_label, message_label, time_label]:
            widget.bind("<Button-1>", mark_as_read)
    
    def on_mark_all_read(self, dropdown):
        """Xử lý đánh dấu tất cả đã đọc."""
        self.controller.mark_all_as_read()
        # Đóng và mở lại dropdown
        if dropdown.winfo_exists():
            dropdown.destroy()
            self.dropdown = None
    
    # ==================== FULL POPUP ====================
    
    def show_full_popup(self):
        """Hiển thị popup với toàn bộ thông báo."""
        from gui.Components.Notification_Full_Popup import NotificationFullPopup
        
        popup = NotificationFullPopup(self.parent, self.controller)
        popup.show()
