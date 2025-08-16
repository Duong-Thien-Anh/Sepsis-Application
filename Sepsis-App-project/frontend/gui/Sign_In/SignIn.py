import customtkinter as ctk
import requests
import os
from dotenv import load_dotenv
from gui.Sign_In.UI_Component import center_desktop , outer_fr_signin, container_fr_signin, layer1_fr_signin, layer2_fr_signin

# Load biến môi trường từ file .env.frontend
load_dotenv(dotenv_path=".env.frontend")
API_URL = os.getenv("API_URL", "http://localhost:8000")  # API backend

class SignInForm(ctk.CTk):
    def __init__(self):
        super().__init__()
        #setting background windows
        self.geometry("862x500")
        self._set_appearance_mode("System")  # or "Light", "Dark"
        self.title("Đăng nhập hệ thống")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
 
        center_desktop(self)
        outer = outer_fr_signin(self)
        container = container_fr_signin(self, outer)
        layer1 = layer1_fr_signin(self,container)
        layer2 = layer2_fr_signin(self,container)

        





    #     # Tiêu đề
    #     self.label_title = ctk.CTkLabel(self, text="Đăng nhập hệ thống", font=("Arial", 20, "bold"))
    #     self.label_title.pack(pady=20)

    #     # Ô nhập username
    #     self.entry_username = ctk.CTkEntry(self, placeholder_text="Tên đăng nhập", width=250)
    #     self.entry_username.pack(pady=10)

    #     # Ô nhập password
    #     self.entry_password = ctk.CTkEntry(self, placeholder_text="Mật khẩu", width=250, show="*")
    #     self.entry_password.pack(pady=10)

    #     # Nút đăng nhập
    #     self.btn_login = ctk.CTkButton(self, text="Đăng nhập", command=self.login)
    #     self.btn_login.pack(pady=20)

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
