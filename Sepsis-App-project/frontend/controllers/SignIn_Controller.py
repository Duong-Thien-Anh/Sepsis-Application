from ast import pattern
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
import requests
import re    
from services.api.config import load_environment, API_URL , TIMEOUT
# from gui.Components.SignIn_Component import layer2_fr_signin, layer3_fr_forgetpassword
# ========== API GETTER FUNCTIONS ==========
def get_api_url():
    """
    Hàm getter để component có thể lấy API_URL
    """
    return API_URL

def get_timeout():
    """
    Hàm getter để component có thể lấy TIMEOUT
    """
    return TIMEOUT

# class SignInController:
#     def __init__(self):
#         load_environment()
#         self.api_url = get_api_url()
#         self.timeout = get_timeout()
#         print(f"Using API: {self.api_url} with timeout: {self.timeout}")
        
# ========== LIMIT USERNAME LENGTH ==========
def validate_username_input(text):
    return len(text) <= 30

def limit_username_length(entry,min_length=0, max_length=30):
    text = entry.get()
    if len(text) > max_length:
        entry.delete(max_length, tk.END)
        entry.configure(text_color="red")
    elif len(text) == min_length:
        entry.configure(text_color="red")
    else:
        entry.configure(text_color="black")

# ========== SET UP USERNAME ==========
def setup_username_entry(entry, placeholder="Nhập username"):
    vcmd = (entry.register(validate_username_input), '%P')
    entry.configure(validate='key', validatecommand=vcmd)

    entry.insert(0, placeholder)
    entry.configure(fg_color="white", text_color="grey")
    entry.bind("<KeyRelease>", lambda event: limit_username_length(entry, max_length=30))

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, ctk.END)
            entry.configure(text_color="black")
    
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(text_color="grey")
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ========== LIMIT PASSWORD LENGTH ==========
def validate_password_input(text):
    return len(text) <= 30

def limit_password_length(entry, min_length=8, max_length=30):
    text = entry.get()
    if len(text) > max_length:
        entry.delete(max_length)
        entry.configure(text_color="red")
    elif len(text) < min_length and len(text) > 0:
        entry.configure(text_color="red")
    else:
        entry.configure(text_color="black")

# ========== SET UP PASSWORD ==========
def toggle_password_visibility(entry, eye_button, state):
    if state["visible"]:  
        entry.configure(show="*")
        eye_button.configure(
        text="👁",
        fg_color="white",
        hover_color="#f0f0f0"
        )
        state["visible"] = False
    else:
        entry.configure(show="")
        eye_button.configure(
        text="🙈",
        fg_color="white",
        hover_color="#f0f0f0"
        )
        state["visible"] = True

def setup_password_entry(entry, placeholder=None, eye_button=None):
    vcmd = (entry.register(validate_password_input), '%P')
    entry.configure(validate='key', validatecommand=vcmd)

    entry.insert(0, placeholder)
    entry.configure(fg_color="white", text_color="grey", show="") 
    entry.bind("<KeyRelease>", lambda event: limit_password_length(entry, min_length=8, max_length=30)) 
    state = {"visible": False} 
    eye_button.configure(command=lambda: toggle_password_visibility(entry, eye_button, state), hover_color="#f0f0f0")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, ctk.END)
            entry.configure(text_color="black", show="*") 

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(text_color="grey", show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)   

# ========== HOVER LABEL ==========
def hover_effect_label_forget_password(label):
    def on_enter(event):
        label.configure(text_color="#fe0707")

    def on_leave(event):
        label.configure(text_color="#66B7FF")

    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)

def login(username , password):
    if not username or not password:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
        return

    try:
        url = f"{API_URL}/auth/login"
        payload = {"username": username, "password": password}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            return f"Đăng nhập thành công! Token: {data['access_token']}"
        else:       
            return f"Đăng nhập thất bại: {response.json().get('detail')}"
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới API backend.\n{e}")

# ========== SHOW FORGET PASSWORD ==========
# def show_signin(self):
#     # Ẩn layer3 nếu có
#     if self.layer3:
#         self.layer3.grid_forget()

#     if not self.layer2:
#         self.layer2 = layer2_fr_signin(self.container, self)  # pass self = controller
#     self.layer2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# def show_forget_password(self):
#     # Ẩn layer2 nếu có
#     if self.layer2:
#         self.layer2.grid_forget()

#     if not self.layer3:
#         self.layer3 = layer3_fr_forgetpassword(self.container, self)
#     self.layer3.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# ========== LIMIT EMAIL LENGTH ==========

def validate_email_format(email: str) -> bool:
    GMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    return re.fullmatch(GMAIL_REGEX, email) is not None

def check_email(entry, error_label, min_length=5, max_length=30):
    text = entry.get()
    if text == "" or text == "Nhập email":
        error_label.configure(text="Vui lòng nhập email." , text_color="red")
        return False
    
    if len(text) > max_length:
        error_label.configure(text = f"Email không được vượt quá {max_length} ký tự." , text_color="red")
        return False
    
    if len(text) < min_length:
        error_label.configure(text = f"Email phải có ít nhất {min_length} ký tự." , text_color="red")
        return False
    
    if not validate_email_format(text):
        error_label.configure(text="Email không hợp lệ, chỉ chấp nhận @gmail.com" , text_color="red")
        return False
    
    else:
        error_label.configure(text="")
        return True

# ========== SET UP EMAIL ==========
def setup_email_entry(entry,error_label, placeholder="Nhập email"):
    def on_validate(new_value):
        if new_value == "" or len(new_value) == placeholder:
            return True
        if len(new_value) > 30:
            return False
        return True
    
    vcmd = (entry.register(on_validate), "%P")
    entry.configure(validate="key", validatecommand=vcmd)

    entry.insert(0, placeholder)
    entry.configure(fg_color="white", text_color="grey")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, ctk.END)
            entry.configure(text_color="black")
    
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(text_color="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ========== CHECK OTP FOR BUTTON SEND CODE ==========
def on_send_code(self , parent):
    if check_email(self.email_entry, self.error_label):
        print("Email hợp lệ → tiếp tục gửi mã")
        # TODO: gọi hàm gửi mã OTP tại đây
        switch_to_code_input(self, parent)
    else:
        print("Email không hợp lệ → dừng lại")     

# ========= SWITCH UI =========
def switch_to_code_input(self, parent):
    """Ẩn input + button cũ → Hiện 4 ô code + button xác nhận"""
    # Xóa widget cũ (entry + button)
    self.email_entry.destroy()
    self.send_button.destroy()
    self.error_label.destroy()
    self.underline_frame.destroy()

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

    self.code_entries = []

    def on_key_release(event, idx):
        value = event.widget.get()

        # Xử lý phím Backspace
        if event.keysym == "BackSpace":
            if value == "" and idx > 0:
                prev_entry = self.code_entries[idx - 1]
                prev_entry.delete(0, ctk.END)
                prev_entry.focus()
            return

        # Nếu nhập nhiều ký tự (paste)
        if len(value) > 1:  
            first_char = value[0]
            event.widget.delete(0, ctk.END)
            event.widget.insert(0, first_char)

            remaining = value[1:]
            next_idx = idx + 1
            while remaining and next_idx < len(self.code_entries):
                next_entry = self.code_entries[next_idx]
                if next_entry.get() == "":
                    next_entry.insert(0, remaining[0])
                    remaining = remaining[1:]
                next_idx += 1

        elif len(value) == 1 and idx < len(self.code_entries) - 1:
            # Nhập 1 ký tự thì nhảy sang ô tiếp theo
            self.code_entries[idx + 1].focus()

    for i in range(4):
        entry = ctk.CTkEntry(
            code_frame,
            width=50,
            height=50,
            justify="center",
            font=("Arial", 18, "bold"),
        )
        entry.grid(row=0, column=i, padx=5)
        entry.bind("<KeyRelease>", lambda e, idx=i: on_key_release(e, idx))
        self.code_entries.append(entry)

    # ---- Button xác nhận ----
    confirm_btn = ctk.CTkButton(
        parent,
        text="Xác nhận",
        fg_color="#66B7FF",
        hover_color="#45a049",
        text_color="white",
        command=lambda: on_confirm_code(self),
        corner_radius=8,
        border_color="#000000",
        border_width=1,
        font=("Arial", 14, "bold"),
        width=100,
        height=45
    )
    confirm_btn.pack(pady=20)


# ========= HANDLE CONFIRM =========
def on_confirm_code(self):
    code = "".join([e.get() for e in self.code_entries])
    if len(code) == 4 and code.isdigit():
        print(f"✅ Code nhập: {code}")
    else:
        print("⚠️ Code chưa hợp lệ")