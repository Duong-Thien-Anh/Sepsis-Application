import customtkinter as ctk
import tkinter as tk
from PIL import Image
# from controllers.Home_Controller import HomeController
from assets.Assets_Management import AssetManager

# ========== DASHBOARD FORM ==========
class HomeFormUI(ctk.CTkFrame):
    def __init__(self,master ,parent_component=None):
        super().__init__(master , fg_color ="#F7F7F5")
        # self.controller = HomeController()
        self.parent_component = parent_component 
        self.pack(fill="both", expand=True)

    # ==========  HEADER ==========
    def create_header(self, layer1):
        layer1.configure(fg_color = "#F7F7F5")

        self.create_breadcrumb(layer1, ["Home"])
        self.create_title(layer1)
        self.create_notification_button(layer1)
        self.create_login_button(layer1)

    # ========== BREADCRUMB =========
    def create_breadcrumb(self ,parent , items):
        """
        Tạo breadcrumb đơn giản (không icon).
        parent : frame cha
        items  : list các nhãn breadcrumb, vd ["Home", "Dashboard", "Current Page"]
        """
        breadcrumb_frame = ctk.CTkFrame(
            parent,
            fg_color="#F7F7F5",
        )
        breadcrumb_frame.grid(row=0, column=0, sticky="w", padx=10)

        for i, crumb in enumerate(items):
            label = ctk.CTkLabel(
                breadcrumb_frame,
                text=crumb,
                font=("Roboto", 15, "bold"),
                text_color="#5D5C5C",
                fg_color="transparent"
            )
            label.grid(row=0, column=i*2, padx=2, pady=5, sticky="w")

            if i < len(items) - 1:  # chưa phải phần tử cuối thì thêm dấu ">"
                separator = ctk.CTkLabel(
                    breadcrumb_frame,
                    text=">",
                    font=("Arial", 12),
                    text_color="#000000",
                    fg_color="#FFFFFF"
                )
                separator.grid(row=0, column=i*2+1, padx=2, pady=5, sticky="w")

        return breadcrumb_frame
    # # ==========  TITLE  ==========
    def create_title(self, parent):
        # Load ảnh
        path = AssetManager.get_image_path("Title_Home")
        icon_image = ctk.CTkImage(
            light_image=Image.open(path),
            dark_image=Image.open(path),
            size=(170,35)  # tuỳ chỉnh kích thước
        )

        # Chèn ảnh (dùng CTkLabel nhưng không cần text)
        image_label = ctk.CTkLabel(
            parent,
            text="",   # không có chữ
            image=icon_image
        )
        image_label.image = icon_image  # giữ reference
        image_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # ==========  BUTTON NOTIFICATION ==========
    def create_notification_button(self, parent):
        # path = AssetManager.get_icon_path("btn_Notification")
        # notif_img = ctk.CTkImage(
        #     light_image=Image.open(path),
        #     dark_image=Image.open(path),
        #     size=(30, 30)  # chỉnh kích thước icon
        # )
        # notif_btn = ctk.CTkLabel(parent, image=notif_img, text="")
        # notif_btn.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        # return notif_btn
        notif_btn = ctk.CTkButton(
        parent,
        text="🔔",
        width=40,
        height=40,
        corner_radius=20,       # = width/2 để tròn
        fg_color="#2196F3",     # màu nền nút
        hover_color="#1976D2",  # màu hover
        text_color="white",
        border_width=0
        )
        notif_btn.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        return notif_btn

    # ==========  BUTTON USER===================
    def create_login_button(self, parent):
        login_btn = ctk.CTkButton(parent, text="Đăng nhập", width=40 , height=40, corner_radius=40 , border_color="#FFFFFF", border_width=1)
        login_btn.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        return login_btn