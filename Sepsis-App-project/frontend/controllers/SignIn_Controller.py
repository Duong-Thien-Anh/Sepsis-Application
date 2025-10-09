from ast import pattern
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
import requests
import re 
from dotenv import load_dotenv

class SignInController():
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
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

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

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)   

    # ========== HOVER LABEL ==========
    def hover_effect_label_forget_password(self, label):
        def on_enter(event):
            label.configure(text_color="#fe0707")

        def on_leave(event):
            label.configure(text_color="#66B7FF")

        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)

    # ========== HANDLE SIGN IN BUTTON CLICK ==========
    
    def login(self, username, password, on_success=None):
        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        try:
            url = f"{self.api_url}/auth/login"
            payload = {"username": username, "password": password}
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                
                # Nếu login thành công -> hiện thông báo và chuyển trang
                messagebox.showinfo("Đăng nhập", "Đăng nhập thành công!")
                
                if on_success:  # Gọi callback để chuyển sang trang Home
                    on_success()
                return True
            else:
                data = response.json()
                messagebox.showerror("Lỗi", data.get('detail', 'Đăng nhập thất bại!'))
                return False
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới API backend.\n{e}")
            return False

    # ========== login_API ==========
    def login1(self, username, password):
        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        try:
            # Gọi API login ở BE (http://localhost:5000/api/auth/login)
            url = f"{self.api_url}/auth/login"
            payload = {"username": username, "password": password}
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                return f"✅ {data['message']} (User: {data.get('user', {}).get('username', 'unknown')})"
            else:
                data = response.json()
                return f"❌ Đăng nhập thất bại: {data.get('detail', 'Unknown error')}"
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới API backend.\n{e}")




