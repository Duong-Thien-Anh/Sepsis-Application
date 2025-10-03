from ast import pattern
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
import requests
import re 
from dotenv import load_dotenv

class HeaderController:
    def __init__(self):
        load_dotenv()
        self.api_url = "http://localhost:5000"  # Thay đổi URL nếu cần
        self.timeout = 5  # Thời gian chờ mặc định

    def on_click(self, event):
        print("🔔 Notification button clicked!")

    def setup_events(self, frame, bell, badge_icon, count=0, command=None):
        """Gắn sự kiện hover + click + badge hiển thị"""

        # Hiển thị badge nếu có thông báo
        if count > 0:
            badge_icon.place(relx=0.75, rely=0.25, anchor="center")
            badge_icon.lift()

        # Hover effect
        def on_enter(e):
            frame.configure(fg_color="#FE5858")   # đỏ khi hover
        def on_leave(e):
            frame.configure(fg_color="white")     # trở về trắng

        # bind hover cho frame và các widget con
        for widget in (frame, bell, badge_icon):
            widget.bind("<Enter>", on_enter)    
            widget.bind("<Leave>", on_leave)

        # Click event
        if command:
            frame.bind("<Button-1>", lambda e: command())

        
    