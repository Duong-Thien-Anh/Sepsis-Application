import customtkinter as ctk
import tkinter as tk
from PIL import Image
from assets.Assets_Management import AssetManager
from gui.Components.Header_Component import HeaderFormUI
from gui.Components.Home_Component import HomeUI
from gui.Components.Ai_Component import AI_UI

# ========== DASHBOARD COMPONENT ==========
class DashBoardComponent(ctk.CTkFrame):
    def __init__(self, master, parent_window=None):
        """
        Component Dashboard chính (CTkFrame).
        
        Args:
            master: Container frame
            parent_window: Frame_DB instance (để gọi logout())
        """
        super().__init__(master)
        
        self.parent_window = parent_window  # Reference để logout

        self.pack(fill="both", expand=True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        outer_DB = self.outer_fr_dashboard()
        container_DB = self.container_fr_dashboard(outer_DB)

        self.layer1_DB = self.layer1_fr_dashboard(container_DB)
        self.layer2_DB = self.layer2_fr_dashboard(container_DB)

        menu_bar = self.menu_bar(outer_DB)
        #maincontent mặc định ở layer 2
        self.show_content(HomeUI)


    # ========== OUTER =====================
    # Outer frame to provide a black border for the window
    def outer_fr_dashboard(self):
        outer_DB = ctk.CTkFrame(
            self,
            fg_color="#66B7FF",
            corner_radius=10,
            border_color="#000000",
            border_width=2,
        )
        outer_DB.grid(row=0, column=0, sticky="nsew")
        outer_DB.grid_rowconfigure(0, weight=1)
        outer_DB.grid_columnconfigure(0, weight=0)
        outer_DB.grid_columnconfigure(1, weight=1)
        return outer_DB

    # ========== MENU BAR ================
    def menu_bar(self, outer_DB , min_w = 80):
        menu_bar = ctk.CTkFrame(
            outer_DB,
            width=min_w,
            fg_color="#66B7FF",   
            corner_radius=15,
            # border_color="#000000",
            # border_width=2,
        )
        menu_bar.grid(row=0, column=0, sticky="nsew",padx=(20,0), pady=20)
        menu_bar.grid_propagate(False)
        menu_bar.grid_rowconfigure(0, weight=1)  
        menu_bar.grid_columnconfigure(0, weight=1) 

        icons = [
            ("btn_Menu", HomeUI, None),
            ("btn_Ai", AI_UI, None),
            ("btn_Patient", HomeUI, None),
            ("btn_Employee", HomeUI, None),
            ("btn_Account", HomeUI, None),
            ("btn_Recall_Appointment", HomeUI, None),
            ("btn_setting", HomeUI, None),
            ("btn_Sign_Out", None, "logout")  # Special: logout action
        ]

        row = 0
        for item in icons:
            key = item[0]
            page_class = item[1]
            action = item[2] if len(item) > 2 else None
            
            try:
                path = AssetManager.get_icon_path(key)
                image = ctk.CTkImage(
                    light_image=Image.open(path),
                    dark_image=Image.open(path),
                    size=(25, 25)  # chỉnh kích thước icon
                )
                
                # Xác định command cho button
                if action == "logout":
                    cmd = self.handle_logout
                elif page_class:
                    cmd = lambda pc=page_class: self.show_content(pc)
                else:
                    cmd = None
                
                btn = ctk.CTkButton(
                    menu_bar,
                    image=image,
                    text="",  # chỉ hiển thị icon, bỏ chữ
                    width=40,
                    height=50,
                    corner_radius=10,
                    fg_color="transparent",  # nền trong suốt
                    hover_color="#FE5858",
                    command=cmd
                )
                btn.grid(row=row, column=0, pady=10, padx=10, sticky="nsew")
                row += 1

            except Exception as e:
                print(f"Lỗi load icon {path}: {e}")

        return menu_bar

    # ========== CONTAINER ================
    def container_fr_dashboard(self, outer_DB):
        container_DB = ctk.CTkFrame(
            outer_DB,
            fg_color="#F7F7F5",   
            corner_radius=15,
            border_color="#000000",
            border_width=2,
        )
        container_DB.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        container_DB.grid_rowconfigure(0, weight=1)  
        container_DB.grid_rowconfigure(1, weight=9)
        container_DB.grid_columnconfigure(0, weight=1)   
        return container_DB

    # ========== LAYER 1 ===========
    def layer1_fr_dashboard(self, container_DB):
        layer1_DB = ctk.CTkFrame(
            container_DB,
            height=50 
        )
        layer1_DB.grid(row=0, column=0, sticky="nsew", padx=(10,10), pady=(10,0)) 
        layer1_DB.grid_propagate(False)
        layer1_DB.pack_propagate(False)

        layer1_DB.grid_rowconfigure(0, weight=1)
        layer1_DB.grid_columnconfigure(0, weight=1)
        layer1_DB.grid_columnconfigure(1, weight=1)
        layer1_DB.grid_columnconfigure(2, weight=0)
        layer1_DB.grid_columnconfigure(3, weight=0)

        #header
        self.header = HeaderFormUI(layer1_DB)
        self.header.create_header(layer1_DB)

        return layer1_DB
    # ========== LAYER 2 ==========
    def layer2_fr_dashboard(self, container_DB):
        layer2_DB = ctk.CTkFrame(
            container_DB,
            fg_color="transparent",
        )
        layer2_DB.grid(row=1, column=0, sticky="nsew", padx=(10,10), pady=(10,10)) 
        layer2_DB.grid_propagate(False)
        layer2_DB.pack_propagate(False)

        return layer2_DB

    # ========== SHOW CONTENT ==========
    def show_content(self,content_class):
        # Xoá nội dung hiện tại trong layer2
        for widget in self.layer2_DB.winfo_children():
            widget.destroy()

        # Tạo và hiển thị nội dung mới
        content = content_class(self.layer2_DB)
        content.pack(fill="both", expand=True)
    
    # ========== HANDLE LOGOUT ==========
    def handle_logout(self):
        """Xử lý đăng xuất - quay về màn hình đăng nhập."""
        # Confirm logout
        from tkinter import messagebox
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            if self.parent_window and hasattr(self.parent_window, 'logout'):
                self.parent_window.logout()
            else:
                print("❌ Không thể đăng xuất: parent_window không có method logout()")



 