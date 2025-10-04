from ast import pattern
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
import requests
import re 
from dotenv import load_dotenv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HomeController:
    def __init__(self):
        load_dotenv()
        self.api_url = "http://localhost:5000"  # Thay đổi URL nếu cần
        self.timeout = 5  # Thời gian chờ mặc định

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