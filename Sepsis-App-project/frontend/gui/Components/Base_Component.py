import customtkinter as ctk
import tkinter as tk
from PIL import Image
from assets.Assets_Management import AssetManager
from gui.Components.ForgetPassword_Component import ForgetPasswordFormUI
from gui.Components.Login_Component import LoginFormUI

# ========== SIGN IN COMPONENT ==========
class SignInComponent(ctk.CTkFrame):
    def __init__(self, master, controller, parent_window=None):
        super().__init__(master)

        self.controller = controller
        self.parent_window = parent_window  # Reference đến Frame_DB
        
        self.pack(fill="both", expand=True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        outer = self.outer_fr_signin()
        container = self.container_fr_signin(outer)

        self.layer1 = self.layer1_fr_signin(container)
        self.layer2 = self.layer2_fr_signin(container)

        self.show_signin_form()

    # ========== OUTER =====================
    def outer_fr_signin(self):
    # Outer frame to provide a black border for the window
        outer = ctk.CTkFrame(
            self,
            fg_color="#66B7FF",
            corner_radius=10,
            border_color="#000000",
            border_width=2,
        )
        outer.grid(row=0, column=0, sticky="nsew")   
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)
        return outer

    # ========== CONTAINER ================
    def container_fr_signin(self, outer ):
        # Container (CTkFrame)
        container = ctk.CTkFrame(
            outer,
            fg_color="#F7F7F5",   
            corner_radius=15,
            border_color="#000000",
            border_width=2,  # Giảm từ 3 xuống 2 để mỏng và liền mạch hơn
        )
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        container.grid_propagate(False)

        container.grid_rowconfigure(0, weight=1)  
        container.grid_columnconfigure(0, weight=1)  
        container.grid_columnconfigure(1, weight=1) 
        return container

    # ========== LAYER 1 ==========
    def layer1_fr_signin(self, container):
        layer1 = ctk.CTkFrame(
            container,
            fg_color="#F7F7F5",
        )
        layer1.grid(row=0, column=0, sticky="nsew", padx=(10,0), pady=10)  # Thêm pady đều để có viền dưới
        layer1.grid_propagate(False)
        layer1.pack_propagate(False)

        try:
            img = ctk.CTkImage(
            light_image=Image.open(AssetManager.get_image_path("SignIn_Pic")), size=(280, 350))
            label_img = ctk.CTkLabel(layer1, image=img, text="")
            label_img.place(relx=0.5, rely=0.5, anchor="center")

        except Exception as e:
            placeholder_label = ctk.CTkLabel(
                layer1,
                text="Lỗi hiển thị",
                font=("Arial", 14),
                text_color="red"
            )
            placeholder_label.place(relx=0.5, rely=0.5, anchor="center")
        return layer1
        
    # ========== LAYER 2 ==========
    def layer2_fr_signin(self, container):

        layer2 = ctk.CTkFrame(
            container,
            fg_color="#F7F7F5",
        )
        layer2.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        layer2.grid_propagate(False)
        layer2.pack_propagate(False)

        return layer2

    # ========== FORM HANDLING ==========
    def show_signin_form(self):
        self.clear_layer2()
        self.current_form = LoginFormUI(
            self.layer2, 
            parent_component=self,
            parent_window=self.parent_window  # Truyền parent_window xuống LoginFormUI
        )
        self.current_form.pack(expand=True, fill="both")

    def show_forgetpassword_form(self):
        self.clear_layer2()
        self.current_form = ForgetPasswordFormUI(
            self.layer2, parent_component=self
        )
        self.current_form.pack(expand=True, fill="both")

    def clear_layer2(self):
        for widget in self.layer2.winfo_children():
            widget.destroy()