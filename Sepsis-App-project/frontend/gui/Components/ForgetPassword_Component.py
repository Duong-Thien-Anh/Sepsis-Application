import customtkinter as ctk
import tkinter as tk
from PIL import Image
from controllers.ForgetPassword_Controller import ForgetPasswordController
from controllers.SignIn_Controller import SignInController

# ========== FORGET PASSWORD FORM ==========
class ForgetPasswordFormUI(ctk.CTkFrame):
    def __init__(self,master ,parent_component=None):
        super().__init__(master)
        self.controller = ForgetPasswordController()
        self.SignIn_Ctrl = SignInController()
        self.parent_component = parent_component  # call show_signin()
        self.pack(fill="both", expand=True)

        # ========== FORM CONTAINER ==========
        self.form_forget_password = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_color="#000000",
            border_width=2,
        )
        self.form_forget_password.pack(expand=True, fill="both", padx=15, pady=15)

        # ========== TITLE ==========
        title_label = ctk.CTkLabel(
            self.form_forget_password,
            text="Quên mật khẩu",
            font=("Arial", 30, "bold"),
            text_color="#000000"
        )
        title_label.pack(pady=(25, 40))

        # ========== INPUTS & BUTTONS ==========
        self.email_entry, self.error_label, self.underline_frame = self.input_email_fr_forgetpassword(self.form_forget_password)
        self.send_button = self.button_send_code_fr_forgetpassword(self.form_forget_password)
        self.back_to_signin_link = self.back_to_signin_fr_forgetpassword(self.form_forget_password)

        self.controller.bind_widgets(
            email_entry=self.email_entry,
            error_label=self.error_label,
            underline_frame=self.underline_frame,
            send_button=self.send_button
        )
    
    # ========== BACK TO SIGN IN LINK ==========
    def back_to_signin_fr_forgetpassword(self, form_forget_password):
        back_to_signin_label = ctk.CTkLabel(
            form_forget_password,
            text="Quay lại đăng nhập",
            font=("Arial", 12, "underline"),
            text_color="#000000",
            cursor="hand2"
        )
        back_to_signin_label.pack(pady=(10, 0))
        self.SignIn_Ctrl.hover_effect_label_forget_password(back_to_signin_label)
        back_to_signin_label.bind("<Button-1>", lambda e: self.parent_component.show_signin_form())
        return back_to_signin_label

    # ========== FORGET PASSWORD  INPUT==========
    def input_email_fr_forgetpassword(self, form_forget_password):
        email_entry = ctk.CTkEntry(
            form_forget_password,
            fg_color="#FFFFFF",
            text_color="#000000",
            font=("Arial", 12),
            border_width=2,
            border_color="#FFFFFF",
            width=200,
            height=40,
        )
        email_entry.pack(pady=(40, 0), padx=35, fill="x")

        underline_frame = ctk.CTkFrame(form_forget_password, height=2, fg_color="#000000")
        underline_frame.pack(padx=35, fill="x")

        error_label = ctk.CTkLabel(form_forget_password, text="", text_color="red", font=("Arial", 10))
        error_label.pack(padx=35, anchor="w")

        self.controller.setup_email_entry(email_entry, error_label, placeholder="Nhập email")
        # email_entry.bind("<Return>", lambda event: self.on_send_code(form_forget_password))
        return email_entry, error_label , underline_frame

    # ========== BUTTON SEND CODE ==========
    def button_send_code_fr_forgetpassword(self, form_forget_password):
        self.send_button = ctk.CTkButton(
            form_forget_password,
            text="Gửi mã",
            fg_color="#66B7FF",
            hover_color="#45a049",
            text_color="white",
            command=lambda: self.controller.on_send_code(form_forget_password),
            corner_radius=8,
            border_color="#000000",
            border_width=1,
            font=("Arial", 14, "bold"),
            width=100,
            height=45
        )
        self.send_button.pack(pady=20)
        return self.send_button