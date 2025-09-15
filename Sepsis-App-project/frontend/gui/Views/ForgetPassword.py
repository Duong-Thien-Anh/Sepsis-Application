import customtkinter as ctk
from gui.Components.SignIn_Component import SignInComponent , ForgetPasswordFormUI

class ForgetPasswordForm(ctk.CTk):
    def __init__(self):
        super().__init__()
        #setting background windows
        self.geometry("862x500")
        self._set_appearance_mode("System")  # or "Light", "Dark"
        self.title("Quên mật khẩu")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
 
        self.center_desktop()

        self.Component = SignInComponent(self)
        self.Component.grid(row=0, column=0, sticky="nsew")  #  Thêm grid cho frame

        self.ForgetPassword = ForgetPasswordFormUI (master=self.Component)
        self.ForgetPassword.grid(row=0, column=0, sticky="nsew")  #  Thêm grid cho UI

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
        
