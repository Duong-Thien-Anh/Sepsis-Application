from ast import pattern
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
import requests
import re 
from dotenv import load_dotenv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from services.api.api_urls import API_ROUTES

class HomeController:
    def __init__(self):
        load_dotenv()
        self.api_url = "http://localhost:5000"  # Thay đổi URL nếu cần
        self.timeout = 2  # Giảm timeout để phản hồi nhanh hơn
        self._cache = {}  # Cache dữ liệu để tránh gọi API nhiều lần

        #========= SHOW BAR CHARTS ==========
    def show_bar_chart(self, parent):
        x = ["A", "B", "C", "D"]
        y = [5, 7, 3, 8]

        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(x, y, color="skyblue")
        ax.set_title("Biểu đồ cột")
        ax.set_xlabel("Danh mục")
        ax.set_ylabel("Giá trị")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)
    
    #========= SHOW PIE CHARTS ==========
    def show_pie_chart(self, parent):
        labels = ["A", "B", "C", "D"]
        sizes = [15, 30, 45, 10]

        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Biểu đồ tròn")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True , padx=4, pady=4)

    def get_patient_count_this_month(self):
        """Lấy số bệnh nhân trong tháng với cache và timeout ngắn"""
        cache_key = "patient_count_month"
        
        # Kiểm tra cache (cache trong 30 giây)
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            import time
            if time.time() - cached_time < 30:  # Cache 30 giây
                print("📦 Sử dụng dữ liệu từ cache")
                return cached_data
        
        try:
            url = API_ROUTES["statistics"]["month"]
            print(f"🌐 Đang gọi API: {url}")
            response = requests.get(url, timeout=self.timeout)
            data = response.json()
            result = data.get("data", 0)
            
            # Lưu vào cache
            import time
            self._cache[cache_key] = (time.time(), result)
            
            return result
        except requests.exceptions.Timeout:
            print("⏰ Timeout khi gọi API (server không phản hồi)")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Không thể kết nối đến server")
            return None
        except Exception as e:
            print(f"❌ Lỗi khi tải dữ liệu bệnh nhân tháng: {e}")
            return None