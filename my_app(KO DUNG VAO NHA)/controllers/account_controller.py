import json
import tkinter as tk
from tkinter import messagebox
from models.data_models import load_users

ACCOUNT_FILE = "account.json"

class AccountController:

    def __init__(self, view):
        self.view = view
        self.users = load_users()
        self.account_data = []
        
    def load_accounts_from_file(self):
        try:
            with open(ACCOUNT_FILE, "r", encoding="utf-8") as f:
                self.account_data = json.load(f)
        except FileNotFoundError:
                self.account_data = []

    def save_accounts_from_file(self):
        try:
            with open(ACCOUNT_FILE, "w", encoding="utf-8") as f:
                json.dump(self.account_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi khi ghi file:", e)
