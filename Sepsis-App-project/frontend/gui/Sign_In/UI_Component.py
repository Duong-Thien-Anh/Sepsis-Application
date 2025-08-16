import customtkinter as ctk
from PIL import Image
from assets.assets import AssetManager

# ========== CENTER DESKTOP ==========
def center_desktop(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Define width and height for centering
        width = 862
        height = 500
        
        # Calculate coordinates for centering
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

# ========== OUTER ==========
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

# ========== CONTAINER ==========
def container_fr_signin(self, outer , w=822, h=460):
    # Container (CTkFrame)
    container = ctk.CTkFrame(
        outer,
        width=w,
        height=h,
        fg_color="#F7F7F5",   
        corner_radius=15,
        border_color="#000000",
        border_width=2,
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
        layer1.grid(row=0, column=0, sticky="nsew", padx=(10,0), pady=(10)) 
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

# ========== INPUT USERNAME ==========
def input_username_fr_signin(self,form_signin):
    username_entry = ctk.CTkEntry(
        form_signin,
        placeholder_text="Tên đăng nhập",
        fg_color="#FFFFFF",
        border_color="#000000",
        border_width=2,
        corner_radius=10,
        width=250,
        height=40,
    )
    username_entry.pack(pady=(10, 0), padx=15, fill="x")
    return username_entry

# ========== INPUT PASSWORD ==========
def eye_button_fr_signin(self , form_signin):
    eye_button = ctk.CTkButton(
        form_signin,
        text="👁️",
        command=lambda: self.toggle_password_visibility()
    )
    eye_button.pack(side="right", padx=(0, 15))
    return eye_button

def input_password_fr_signin(self, form_signin):
    password_frame = ctk.CTkFrame(form_signin , fg_color="transparent")
    password_frame.pack(pady=(5, 5), padx=15, fill="x")

    password_entry = ctk.CTkEntry(
        form_signin,
        placeholder_text="Mật khẩu",
        fg_color="#FFFFFF",
        border_color="#000000",
        border_width=2,
        corner_radius=10,
        width=250,
        height=40,
        show="*"
    )
    password_entry.pack(side="left", fill="x", expand=True)
    self.eye_button = eye_button_fr_signin(self, password_frame)
    return password_entry

# ========== TOGGLE PASSWORD ==========


# ========== LAYER 2 ==========
def layer2_fr_signin(self,container):
 
        layer2 = ctk.CTkFrame(
            container,
            fg_color="#F7F7F5",
        )
        layer2.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        layer2.grid_propagate(False)
        layer2.pack_propagate(False)

        try:
            form_signin = ctk.CTkFrame(
                layer2,
                fg_color="#F7F7F5",
                corner_radius=15,
                border_color="#000000",
                border_width=2,

            )
            form_signin.pack(expand=True, fill="both", padx=15, pady=15)
            title_label = ctk.CTkLabel(form_signin,text="Đăng nhập", font=("Arial", 30, "bold" ),text_color="#000000")
            title_label.pack(pady=(25, 0))
            self.username = input_username_fr_signin(self, form_signin)
            self.password = input_password_fr_signin(self, form_signin)

        except Exception as e:
            signin_label = ctk.CTkLabel(
                form_signin,
                text="Lỗi hiển thị",
                font=("Arial", 12),
                text_color="red"
            )
            signin_label.place(relx=0.5, rely=0.5, anchor="center")
        return layer2