import customtkinter as ctk
import tkinter as tk
from PIL import Image
from controllers.ForgetPassword_Controller import ForgetPasswordController
from controllers.Login_Controller import LoginController

# ========== FORGET PASSWORD FORM ==========
class ForgetPasswordFormUI(ctk.CTkFrame):
    def __init__(self,master ,parent_component=None):
        super().__init__(master , fg_color ="#F7F7F5")
        self.ForgetPW_Ctrl = ForgetPasswordController()
        # optional: allow controller to call back component if needed
        try:
            self.ForgetPW_Ctrl.component = self
        except Exception:
            pass
        self.Login_Ctrl = LoginController()
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

        self.ForgetPW_Ctrl.bind_widgets(
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

        self.ForgetPW_Ctrl.setup_email_entry(email_entry, error_label, placeholder="Nhập email")
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
            command=self.on_send_click,  # component handles flow
            corner_radius=8,
            border_color="#000000",
            border_width=2,
            font=("Arial", 14, "bold"),
            width=100,
            height=45
        )
        self.send_button.pack(pady=(30))
        return self.send_button

    def on_send_click(self):
        # use controller only for validation; component performs UI switch
        try:
            ok = False
            if hasattr(self.ForgetPW_Ctrl, "check_email"):
                ok = self.ForgetPW_Ctrl.check_email(self.email_entry, self.error_label)
            else:
                # fallback: simple non-empty check
                txt = self.email_entry.get().strip()
                ok = bool(txt and txt != "Nhập email")
                if not ok:
                    self.error_label.configure(text="Email không hợp lệ", text_color="red")
            if ok:
                # destroy current widgets and show code inputs
                self.switch_to_code_input_form(self.form_forget_password)
        except Exception as e:
            print("on_send_click error:", e)

    # ========== CREATE CODE INPUTS ==========
    def create_code_inputs(self, parent):
        # tạo 4 ô nhập code bên trong parent (được truyền vào)
        self.code_entries = []
        for i in range(4):
            entry = ctk.CTkEntry(
                parent,
                width=50,
                height=50,
                justify="center",
                font=("Arial", 18, "bold"),
            )
            entry.grid(row=0, column=i, padx=5)
            entry.bind("<KeyRelease>", lambda e, idx=i: getattr(self.ForgetPW_Ctrl, "on_key_release", lambda *_: None)(e, idx))
            self.code_entries.append(entry)

        # cho controller biết danh sách entry (nếu controller xử lý on_confirm/on_key)
        try:
            self.ForgetPW_Ctrl.code_entries = self.code_entries
        except Exception:
            pass

        # ---- Button xác nhận ----
        confirm_btn = ctk.CTkButton(
            parent,
            text="Xác nhận",
            fg_color="#66B7FF",
            hover_color="#45a049",
            text_color="white",
            # gọi controller.on_confirm_code() trực tiếp hoặc gọi 1 hàm của component nếu muốn xử lý UI
            command=lambda: getattr(self.ForgetPW_Ctrl, "on_confirm_code", lambda : None)(),
            corner_radius=8,
            border_color="#000000",
            border_width=2,
            font=("Arial", 14, "bold"),
            width=100,
            height=45
        )
        confirm_btn.grid(row=1, column=0, columnspan=4, pady=20) 
          

    # ========== SWITCH UI ==========
    def switch_to_code_input_form(self, parent):
        """Ẩn input + button cũ → Hiện 4 ô code + button xác nhận"""
        # Xoá các widget cũ (component tự xoá để tránh dependency / exception từ controller)
        for attr in ("email_entry", "send_button", "error_label", "underline_frame", "back_to_signin_link"):
            w = getattr(self, attr, None)
            if w:
                try:
                    w.destroy()
                except Exception:
                    pass
                setattr(self, attr, None)

        # tiêu đề
        title_label = ctk.CTkLabel(
            parent,
            text="Vui lòng nhập mã xác nhận !",
            font=("Arial", 20, "bold"),
            text_color="#66B7FF",
        )
        title_label.pack(pady=(25, 0))

        # ---- 4 ô nhập code ----
        code_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
        code_frame.pack(pady=(20, 10))
        # tạo các input và button confirm bên component
        self.create_code_inputs(code_frame)
        self.back_to_signin_link = self.back_to_signin_fr_forgetpassword(parent)


