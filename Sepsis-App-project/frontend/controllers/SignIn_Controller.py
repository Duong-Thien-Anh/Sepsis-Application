from ast import pattern
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
import requests
import re    
from services.api.config import load_environment, API_URL , TIMEOUT

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

# ========== LIMIT EMAIL LENGTH ==========

def validate_email_format(email: str) -> bool:
    GMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    GMAIL_REGEX = pattern
    return re.match(pattern, email) is not None

def check_email(entry, min_length=5, max_length=30):
    text = entry.get()
    if len(text) > max_length:
        entry.delete(max_length, tk.END)
        entry.configure(text_color="red")
    elif len(text) < min_length:
        entry.configure(text_color="red")
    elif not validate_email_format(text):
        entry.configure(text_color="red")
    else:
        entry.configure(text_color="black")


# ========== SET UP EMAIL ==========
def setup_email_entry(entry, placeholder="Nhập email"):
    vcmd = (entry.register(validate_email_format), '%P')
    entry.configure(validate='key', validatecommand=vcmd)

    entry.insert(0, placeholder)
    entry.configure(fg_color="white", text_color="grey")
    entry.bind("<KeyRelease>", lambda event: check_email(entry, max_length=30))

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