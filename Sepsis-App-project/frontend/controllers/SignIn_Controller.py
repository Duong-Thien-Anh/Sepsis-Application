from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
import requests    
from services.API import load_environment 

def limit_username_length(entry, max_length=30):
    def on_key_press(event):
        if len(entry.get()) >= max_length and event.keysym != 'BackSpace':
            return "break"  
    entry.bind('<KeyPress>', on_key_press)

def setup_username_entry(entry, placeholder="Nhập username"):
    entry.insert(0, placeholder)
    entry.configure(fg_color="white", text_color="grey")
    limit_username_length(entry)

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


def setup_password_entry(entry, placeholder="Nhập mật khẩu"):
    entry.insert(0, placeholder)
    entry.configure(fg_color="white", text_color="grey", show="")  # show="" để hiển thị placeholder
    
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, ctk.END)
            entry.configure(text_color="black", show="*")  # ẩn mật khẩu
    
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(text_color="grey", show="")  # hiện placeholder
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def hover_effect_label_forget_password(label):
    def on_enter(event):
        label.configure(text_color="#fe0707")

    def on_leave(event):
        label.configure(text_color="#66B7FF")

    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)

# def login(self):
#     username = self.entry_username.get().strip()
#     password = self.entry_password.get().strip()

#     if not username or not password:
#         messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
#         return

#     try:
#         url = f"{API_URL}/login"  # endpoint backend
#         payload = {"username": username, "password": password}
#         response = requests.post(url, json=payload)

#         if response.status_code == 200:
#             data = response.json()
#             messagebox.showinfo("Thành công", f"Xin chào {data.get('full_name', username)}!")
#         else:
#             messagebox.showerror("Lỗi đăng nhập", response.json().get("message", "Sai tài khoản hoặc mật khẩu"))
#     except Exception as e:
#         messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới API backend.\n{e}")