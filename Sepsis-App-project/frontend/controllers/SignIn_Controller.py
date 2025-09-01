from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
import requests    
from services.api.config import load_environment, API_URL , TIMEOUT
from services.api.auth_service import AuthService
import webbrowser

GOOGLE_LOGIN_URL = "http://127.0.0.1:5000/api/auth/google/login"
auth_service = AuthService()

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

def login(username, password):
    """
    Xử lý logic đăng nhập: gọi API, lưu token và trả về True/False.
    """
    # 1. Kiểm tra dữ liệu đầu vào từ người dùng
    if not username or not password:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
        return False # Trả về False khi thất bại

    # 2. Gọi API và xử lý kết quả
    try:
        # Gọi phương thức login đã được định nghĩa trong APIClient
        result = auth_service.login(username, password)

        # Lấy access_token từ dữ liệu trả về
        access_token = result.get("access_token")

        if access_token:
            # BƯỚC QUAN TRỌNG: Lưu token vào client để dùng cho các yêu cầu sau
            auth_service.client.set_token(access_token)
            
            print("Đăng nhập thành công, token đã được lưu vào APIClient.")
            return True # Trả về True khi mọi thứ thành công
        else:
            # Trường hợp hiếm: API không báo lỗi nhưng cũng không trả về token
            messagebox.showerror("Lỗi Phản Hồi", "Phản hồi từ server không hợp lệ.")
            return False

    except Exception as e:
        # Bắt lỗi từ APIClient (ví dụ: ConnectionError) và các lỗi khác
        messagebox.showerror("Lỗi Đăng Nhập", f"Đăng nhập thất bại.\nChi tiết: {e}")
        return False

def handle_google_signin_click():
    """
    Mở trình duyệt để bắt đầu quy trình đăng nhập Google.
    """
    print(f"Mở trình duyệt để đăng nhập Google...")
    try:
        webbrowser.open(GOOGLE_LOGIN_URL)
    except Exception as e:
        print(f"Lỗi không thể mở trình duyệt: {e}")