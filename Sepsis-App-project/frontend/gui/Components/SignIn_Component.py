import customtkinter as ctk
from PIL import Image
from assets.assets import AssetManager
from controllers.SignIn_Controller import limit_username_length , setup_username_entry , setup_password_entry , hover_effect_label_forget_password

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
        fg_color="#FFFFFF",
        text_color="#000000",
        font=("Arial", 12),
        border_width=2,
        border_color="#FFFFFF",
        width=200,
        height=40,
    )
    username_entry.pack(pady=(40, 0), padx=35, fill="x")
    setup_username_entry(username_entry, placeholder="Nhập tên đăng nhập")

    underline_frame = ctk.CTkFrame(
         form_signin,
         height=2,
         fg_color="#000000"
    )
    underline_frame.pack( padx=35, fill="x")
    return username_entry

# ========== INPUT PASSWORD ==========
def input_password_fr_signin(self, form_signin):
    password_frame = ctk.CTkFrame(
        form_signin,
        fg_color="transparent"
    )
    password_frame.pack(pady=(10, 0), padx=35, fill="x")

    password_entry = ctk.CTkEntry(
        password_frame,
        fg_color="#FFFFFF",
        text_color="#000000",
        font=("Arial", 12),
        border_width=2,
        border_color="#FFFFFF",
        width=170,
        height=40,
        show="*"
    )
    password_entry.pack(side="left" ,pady=(10, 0), fill="x" , expand=True)
    setup_password_entry(password_entry, placeholder="Mật khẩu")

    eye_button = ctk.CTkButton(
        password_frame,
        text="👁",
        command=lambda: setup_password_entry(password_entry ,eye_button),
        width=30,
        height=30,
        fg_color="white",
        text_color="black",
        corner_radius=5,
        font=("Arial", 18, "bold")
    )
    eye_button.pack(side="right", padx=(5, 0))
    
    underline_frame = ctk.CTkFrame(
        form_signin,
        height=2,
        fg_color="#000000",
    )
    underline_frame.pack( padx=35, fill="x")
    return password_entry, eye_button

# ========== BUTTON SIGN IN ==========
def button_signin_fr_signin(self, form_signin):
    signin_button = ctk.CTkButton(
        form_signin,
        text="Đăng nhập",
        command=lambda: self.signin() if hasattr(self, 'signin') else print("Chức năng đăng nhập chưa được định nghĩa"),
        fg_color="#66B7FF",
        hover_color="#45a049",
        text_color="white",
        corner_radius=8,
        border_color="#000000",
        border_width=1,
        font=("Arial", 14, "bold"),
        width=200,
        height=45
    )
    signin_button.pack(pady=(20, 0), padx=35, fill="x")
    return signin_button

# ========== BUTTON GMAIL ==========
def button_gmail_fr_signin(self, form_signin):
    try:
        gmail_icon = ctk.CTkImage(
            light_image=Image.open(AssetManager.get_image_path("Gmail_Icon")),
            size=(20, 20)
        )
        gmail_button = ctk.CTkButton(
            form_signin,
            text="  Đăng nhập với Gmail",
            image=gmail_icon,
            compound="left",
            command=lambda: self.signin() if hasattr(self, 'signin') else print("Chức năng đăng nhập chưa được định nghĩa"),
            fg_color="#66B7FF",
            hover_color="#45a049",
            text_color="white",
            corner_radius=8,
            border_color="#000000",
            border_width=1,
            font=("Arial", 14, "bold"),
            width=200,
            height=45
        )
    except Exception as e:
        gmail_button = ctk.CTkButton(
            form_signin,
            text="Lỗi hiển thị",
            fg_color="#66B7FF",
            hover_color="#45a049",
            text_color="red",
            corner_radius=8,
            border_color="#000000",
            border_width=1,
            font=("Arial", 14),
            width=200,
            height=45
        )

    gmail_button.pack(pady=(10, 0), padx=35, fill="x")
    return gmail_button

# ========== FORGET PASSWORD ==========
def forget_password_fr_signin(self, form_signin):
    forget_password_link = ctk.CTkLabel(
        form_signin,
        text="Quên mật khẩu?",
        text_color="#66B7FF",
        font=("Arial", 12, "underline"),
    )
    forget_password_link.pack(pady=(5, 0), padx=35, fill="x")
    hover_effect_label_forget_password(forget_password_link)
    return forget_password_link

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
                fg_color="#FFFFFF",
                corner_radius=15,
                border_color="#000000",
                border_width=2,

            )
            form_signin.pack(expand=True, fill="both", padx=15, pady=15)
            title_label = ctk.CTkLabel(form_signin,text="Đăng nhập", font=("Arial", 30, "bold" ),text_color="#000000")
            title_label.pack(pady=(25, 0))
            self.username = input_username_fr_signin(self, form_signin)
            self.password = input_password_fr_signin(self, form_signin)
            self.signin_button = button_signin_fr_signin(self, form_signin)
            self.gmail_button = button_gmail_fr_signin(self, form_signin)
            self.forget_password_link = forget_password_fr_signin(self, form_signin)

        except Exception as e:
            signin_label = ctk.CTkLabel(
                form_signin,
                text="Lỗi hiển thị",
                font=("Arial", 12),
                text_color="red"
            )
            signin_label.place(relx=0.5, rely=0.5, anchor="center")
        return layer2