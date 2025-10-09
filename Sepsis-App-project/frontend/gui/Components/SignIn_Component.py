import customtkinter as ctk
import tkinter as tk
from PIL import Image
from controllers.SignIn_Controller import SignInController
from assets.Assets_Management import AssetManager
from gui.Components.Base_DB_Component import DashBoardComponent

# ========== SIGN IN FORM ==========
class SignInFormUI(ctk.CTkFrame):
    def __init__(self,master ,parent_component=None):
        super().__init__(master, fg_color ="#F7F7F5")
        self.controller = SignInController()
        self.parent_component = parent_component  # call show_forgetpassword()
        self.pack(fill="both", expand=True)

        # ========== FORM CONTAINER ==========
        self.form_signin = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_color="#000000",
            border_width=2,
        )
        self.form_signin.pack(expand=True, fill="both", padx=15, pady=15)

        # ========== TITLE ==========
        title_label = ctk.CTkLabel(
            self.form_signin,
            text="Đăng nhập",
            font=("Arial", 30, "bold"),
            text_color="#000000"
        )
        title_label.pack(pady=(25, 0))

        # ========== INPUTS & BUTTONS ==========
        self.username = self.input_username_fr_signin(self.form_signin)
        self.password = self.input_password_fr_signin(self.form_signin)
        self.signin_button = self.button_signin_fr_signin(self.form_signin)
        self.gmail_button = self.button_gmail_fr_signin(self.form_signin)
        self.forget_password_link = self.forget_password_fr_signin(self.form_signin)

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
        self.controller.setup_username_entry(username_entry, placeholder="Nhập tên đăng nhập")

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


        eye_button = ctk.CTkButton(
            password_frame,
            text="👁",
            command=lambda: self.controller.toggle_password_visibility(password_entry, eye_button, state={"visible": False}),
            width=30,
            height=30,
            fg_color="white",
            text_color="black",
            corner_radius=5,
            font=("Arial", 18, "bold")
        )
        eye_button.pack(side=tk.RIGHT, padx=(5, 0))
        self.controller.setup_password_entry(password_entry, placeholder="Mật khẩu", eye_button=eye_button)

        underline_frame = ctk.CTkFrame(
            form_signin,
            height=2,
            fg_color="#000000",
        )
        underline_frame.pack( padx=35, fill="x")
        return password_entry

    # ========== BUTTON SIGN IN ==========
    def button_signin_fr_signin(self, form_signin):
        signin_button = ctk.CTkButton(
            form_signin,
            text="Đăng nhập",
            command=lambda: self.handle_signin_click(),
            fg_color="#66B7FF",
            hover_color="#45a049",
            text_color="white",
            corner_radius=8,
            border_color="#000000",
            border_width=2,
            font=("Arial", 14, "bold"),
            width=200,
            height=45
        )
        signin_button.pack(pady=(20, 0), padx=35, fill="x")
        return signin_button

    def handle_signin_click(self):
        username = ""
        if hasattr(self, 'username'):
            if isinstance(self.username, tuple):
                username = self.username[0].get()
            else:
                username = self.username.get()

        password = ""
        if hasattr(self, 'password'):
            if isinstance(self.password, tuple):
                password = self.password[0].get()
            else:
                password = self.password.get()

        if username == "Nhập tên đăng nhập":
            username = ""
        if password == "Mật khẩu":
            password = ""
        
        #========== LOGIN FUNCTION ==========
        try : 
            result = self.controller.login1(username.strip(), password.strip())

        except NameError:
            print("Lỗi: Chưa định nghĩa hàm đăng nhập.")
            return 
        except  Exception as e:
            print(f"Lỗi khi gọi hàm đăng nhập: {e}")
            return

        # Xử lý kết quả đăng nhập

        if result is None:
            print("Lỗi: Kết quả đăng nhập trả về None.")
        elif "Đăng nhập thành công" in result.lower():

            print(f"Kết quả đăng nhập: {result}")
            # Ẩn form đăng nhập
            self.pack_forget()

            # Hiển thị giao diện chính (DashBoardComponent)
            try:
                self.dashboard = DashBoardComponent(self.master)
                self.dashboard.pack(fill="both", expand=True)
                print("✅ Chuyển sang giao diện chính thành công.")
            except Exception as e:
                print(f"❌ Lỗi khi mở DashBoardComponent: {e}")

        else:
            print(f"Kết quả đăng nhập không đúng: {result}")
        # Hiển thị thông báo lỗi
        if "Đăng nhập thất bại" in result or "Lỗi kết nối" in result:
            tk.messagebox.showerror("Lỗi đăng nhập", result)

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
                command=lambda: self.signin() if hasattr(self, 'signin') else print("Lỗi: Chức năng đăng nhập chưa được định nghĩa"),
                fg_color="#66B7FF",
                hover_color="#45a049",
                text_color="white",
                corner_radius=8,
                border_color="#000000",
                border_width=2,
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
        self.controller.hover_effect_label_forget_password(forget_password_link)
        def on_click(event=None):
            try:
                if self.parent_component and hasattr(self.parent_component, "show_forgetpassword_form"):
                    self.parent_component.show_forgetpassword_form()
                else:
                    print("No parent_component or show_forgetpassword_form not found")
            except Exception as e:
                print("Error switching to forget password form:", e)

        forget_password_link.bind("<Button-1>", on_click)
        return forget_password_link

 