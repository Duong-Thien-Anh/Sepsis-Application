from ast import pattern
import customtkinter as ctk
import tkinter as tk
import requests
import re 
from dotenv import load_dotenv
from services.api.auth_service import auth_service

class LoginController():
    def __init__(self, api_url=None, timeout=5):
        self.api_url = api_url or "http://localhost:5000/api"
        self.timeout = timeout
        print(f"Using API: {self.api_url} with timeout: {self.timeout}")
        
    # ========== LIMIT USERNAME LENGTH ==========
    def validate_username_input(self,text):
        return len(text) <= 30

    def limit_username_length(self, entry,min_length=0, max_length=30):
        text = entry.get()
        if len(text) > max_length:
            entry.delete(max_length, tk.END)
            entry.configure(text_color="red")
        elif len(text) == min_length:
            entry.configure(text_color="red")
        else:
            entry.configure(text_color="black")

    # ========== SET UP USERNAME ==========
    def setup_username_entry(self, entry, placeholder="Nhập username"):
        vcmd = (entry.register(self.validate_username_input), '%P')
        entry.configure(validate='key', validatecommand=vcmd)

        entry.insert(0, placeholder)
        entry.configure(fg_color="white", text_color="grey")
        entry.bind("<KeyRelease>", lambda event: self.limit_username_length(entry, max_length=30))

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, ctk.END)
                entry.configure(text_color="black")
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(text_color="grey")
        
        # Enable Ctrl+V paste
        def on_paste(event):
            try:
                clipboard_text = entry.clipboard_get()
                # Xóa placeholder nếu có
                if entry.get() == placeholder:
                    entry.delete(0, ctk.END)
                    entry.configure(text_color="black")
                # Chỉ paste tối đa 30 ký tự
                if len(clipboard_text) <= 30:
                    entry.insert(tk.INSERT, clipboard_text)
                else:
                    entry.insert(tk.INSERT, clipboard_text[:30])
                return "break"  # Ngăn default paste behavior
            except:
                pass
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<Control-v>", on_paste)  # Windows/Linux
        entry.bind("<Command-v>", on_paste)  # macOS

    # ========== LIMIT PASSWORD LENGTH ==========
    def validate_password_input(self, text):
        return len(text) <= 30

    def limit_password_length(self, entry, min_length=8, max_length=30):
        text = entry.get()
        if len(text) > max_length:
            entry.delete(max_length , tk.END)
            entry.configure(text_color="red")
        elif len(text) < min_length and len(text) > 0:
            entry.configure(text_color="red")
        else:
            entry.configure(text_color="black")

    # ========== SET UP PASSWORD ==========
    def toggle_password_visibility(self, entry, eye_button, state):
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

    def setup_password_entry(self, entry, placeholder=None, eye_button=None):
        vcmd = (entry.register(self.validate_password_input), '%P')
        entry.configure(validate='key', validatecommand=vcmd)

        entry.insert(0, placeholder)
        entry.configure(fg_color="white", text_color="grey", show="") 
        entry.bind("<KeyRelease>", lambda event: self.limit_password_length(entry, min_length=8, max_length=30)) 
        state = {"visible": False}
        if eye_button: 
            eye_button.configure(command=lambda: self.toggle_password_visibility(entry, eye_button, state), hover_color="#f0f0f0")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, ctk.END)
                entry.configure(text_color="black", show="*") 

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(text_color="grey", show="")

        # Enable Ctrl+V paste for password
        def on_paste(event):
            try:
                clipboard_text = entry.clipboard_get()
                # Xóa placeholder nếu có
                if entry.get() == placeholder:
                    entry.delete(0, ctk.END)
                    entry.configure(text_color="black", show="*")
                # Chỉ paste tối đa 30 ký tự
                if len(clipboard_text) <= 30:
                    entry.insert(tk.INSERT, clipboard_text)
                else:
                    entry.insert(tk.INSERT, clipboard_text[:30])
                return "break"  # Ngăn default paste behavior
            except:
                pass

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<Control-v>", on_paste)  # Windows/Linux
        entry.bind("<Command-v>", on_paste)  # macOS   

    # ========== HOVER LABEL ==========
    def hover_effect_label_forget_password(self, label):
        def on_enter(event):
            label.configure(text_color="#fe0707")

        def on_leave(event):
            label.configure(text_color="#66B7FF")

        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)

    # ========== login_API ==========
    def login1(self, username, password):
        # 1. Validate input ở Controller layer (business logic)
        if not username or not password:
            return "error", "Thiếu thông tin đăng nhập"

        # 2. Gọi API login
        try:
            url = f"{self.api_url}/auth/login"
            payload = {"username": username, "password": password}
            response = requests.post(url, json=payload, timeout=self.timeout)
            data = response.json()
            
            # 3. Xử lý response từ backend (format: {status, data, message})
            if response.status_code == 200 and data.get("status") == 200:
                # Lưu token nếu cần
                if "data" in data and "access_token" in data["data"]:
                    # TODO: Lưu token vào session/storage
                    pass
                return "success", data
            else:
                error_message = data.get('message', 'Sai thông tin đăng nhập')
                return "error", error_message
            
        except requests.exceptions.Timeout:
            return "error", f"Timeout: Không thể kết nối tới server sau {self.timeout}s"
        
        except requests.exceptions.ConnectionError:
            return "error", "Không thể kết nối tới API backend. Vui lòng kiểm tra server."
        
        except Exception as e:
            return "error", f"Lỗi không xác định: {str(e)}"




