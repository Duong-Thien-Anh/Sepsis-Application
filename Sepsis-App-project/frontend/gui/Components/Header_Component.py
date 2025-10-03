import customtkinter as ctk
import tkinter as tk
from PIL import Image , ImageTk , ImageDraw, ImageOps
from controllers.Header_Controller import HeaderController
from assets.Assets_Management import AssetManager

# ========== DASHBOARD FORM ==========
class HeaderFormUI(ctk.CTkFrame):
    def __init__(self,master ,parent_component=None):
        super().__init__(master , fg_color ="#F7F7F5")
        self.Header_Ctrl = HeaderController()
        # optional: allow controller to call back component if needed
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
    def create_notification_button(self, parent, count=0, command=None):
        # ========== LOAD ICON ==========
        path_bell = AssetManager.get_icon_path("icon_Bell")
        bell_img = Image.open(path_bell).resize((30, 30))
        bell_ctk = ctk.CTkImage(bell_img)

        # ========== FRAME chứa ==========
        frame = ctk.CTkFrame(parent, fg_color="white", width=50, height=50 , corner_radius=30 , border_color="black", border_width=2)
        frame.image_refs = ( bell_ctk)  # giữ reference

        # Chuông nằm giữa
        bell = ctk.CTkLabel(frame, image=bell_ctk, text="", fg_color="transparent")
        bell.place(relx=0.5, rely=0.5, anchor="center")

        # Badge đỏ (ảnh PNG) đặt ở góc phải trên
        badge_icon = ctk.CTkFrame(frame, fg_color="red", width=15, height=15 , corner_radius=15 , border_color="black", border_width=2)

        self.Header_Ctrl.setup_events(frame, bell, badge_icon, count, command)

        frame.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        return frame

    # ==========  BUTTON USER===================
    def make_rounded_avatar(self, path, size=(50, 50), border=2, border_color="#FE5858"):
        # Mở ảnh gốc và resize
        img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)

        # Kích thước có viền
        new_size = (size[0] + 2*border, size[1] + 2*border)

        # Tạo ảnh rỗng với nền trong suốt
        final_img = Image.new("RGBA", new_size, (0, 0, 0, 0))

        # Tạo mask hình tròn
        mask = Image.new("L", new_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, new_size[0], new_size[1]), fill=255)

        # Vẽ hình tròn viền (màu border)
        border_layer = Image.new("RGBA", new_size, border_color)
        border_layer.putalpha(mask)
        final_img.paste(border_layer, (0, 0), border_layer)

        # Vẽ ảnh avatar ở giữa
        mask_inner = Image.new("L", size, 0)
        draw_inner = ImageDraw.Draw(mask_inner)
        draw_inner.ellipse((0, 0, size[0], size[1]), fill=255)
        final_img.paste(img, (border, border), mask=mask_inner)
        
        return final_img

    def create_profile_card(self, parent, name, role):
        """
        Tạo card avatar + tên + vai trò
        :param parent: frame cha
        :param avatar_path: đường dẫn ảnh avatar
        :param name: tên hiển thị
        :param role: vai trò (@admin, @user,...)
        """
        frame = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=10)

        # ===== Avatar =====
        avatar_path = AssetManager.get_image_path("Avatar_Default")
        rounded_img = self.make_rounded_avatar(avatar_path, size=(50, 50), border=2, border_color="#FE5858")
        avatar_img = ctk.CTkImage(
            light_image=rounded_img,
            dark_image=rounded_img,
            size=(46, 46),  # avatar tròn kích thước hiển thị
        )
        avatar_label = ctk.CTkLabel(frame, image=avatar_img, text="")
        avatar_label.image = avatar_img  # giữ reference tránh GC
        avatar_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # ===== Tên =====
        name_label = ctk.CTkLabel(
            frame, text=name,
            font=("Arial", 15, "bold"),
            text_color="black"
        )
        name_label.grid(row=0, column=1, sticky="w", padx=(0, 10))

        # ===== Vai trò =====
        role_label = ctk.CTkLabel(
            frame, text=role,
            font=("Arial", 12),
            text_color="gray"
        )
        role_label.grid(row=1, column=1, sticky="w", padx=(0, 10))

        return frame


    # ==========  BUTTON USER ===================
    def create_login_button(self, layer1):
        profile = self.create_profile_card(
            parent=layer1,
            
            name="Duong Thien Anh",
            role="@admin"
        )
        profile.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        return profile

