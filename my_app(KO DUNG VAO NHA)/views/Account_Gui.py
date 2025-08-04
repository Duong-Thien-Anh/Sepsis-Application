import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from models.data_models import load_users
from customtkinter import CTkButton, CTkImage, CTkFrame, CTkScrollbar
import customtkinter as ctk
from controllers.account_controller import AccountController

class AccountListGui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="white")
        self.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.canvas = None
        self.scrollable_frame = None
        self.ctk_widgets = []  # Thêm list để theo dõi CTk widgets  
        self.account_data = []
        self.account_controller = AccountController()
        self.load_data_account_from_file()          
        # Đảm bảo CustomTkinter đã được khởi tạo
        if not hasattr(ctk, '_root_set'):
            try:
                ctk.set_appearance_mode("light")
                ctk.set_default_color_theme("blue")
                ctk._root_set = True
            except:
                pass
        
        self.build_ui()
    
    def load_data_account_from_file(self):
        self.account_data = AccountController.load_accounts_from_file()

    def save_data_account_to_file(self):
        AccountController.save_accounts_to_file(self.account_data)

    def safe_destroy_widgets(self):
        """Safely destroy widgets, especially CTk widgets"""
        try:
            # Destroy CTk widgets first
            for widget in self.ctk_widgets:
                try:
                    if widget.winfo_exists():
                        widget.destroy()
                except:
                    pass
            self.ctk_widgets.clear()
            
            # Then destroy regular tkinter widgets
            for widget in self.winfo_children():
                try:
                    widget.destroy()
                except:
                    pass
        except:
            pass

    def build_ui(self):
        # Safely clear existing widgets
        self.safe_destroy_widgets()
            
        table_header = tk.Frame(self, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        try:
            add_button = ctk.CTkButton(master=table_header, text="➕ Thêm tài khoản", width=150, height=35,
                                   fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5, 
                                   command=self.add_new_account)
            add_button.pack(side=tk.RIGHT, pady=10)
            self.ctk_widgets.append(add_button)  # Thêm vào list

            export_button = ctk.CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35,
                                      fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
                                      command=self.export_json)
            export_button.pack(side=tk.RIGHT, padx=10, pady=10)
            self.ctk_widgets.append(export_button)  # Thêm vào list
        except Exception as e:
            print(f"Lỗi tạo CTk buttons: {e}")
            # Fallback to regular tkinter buttons
            add_button = tk.Button(table_header, text="➕ Thêm tài khoản", bg="#28a745", fg="white",
                                 command=self.add_new_account)
            add_button.pack(side=tk.RIGHT, pady=10)
            
            export_button = tk.Button(table_header, text="📄 Xuất file Json", bg="#ffc107", fg="white",
                                    command=self.export_json)
            export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        title_label = tk.Label(table_header, text="Danh sách tài khoản hệ thống", font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Container
        try:
            table_container = ctk.CTkFrame(self, border_width=1, corner_radius=10)
            table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            self.ctk_widgets.append(table_container)  # Thêm vào list

            # Header row
            header_frame = ctk.CTkFrame(table_container, fg_color="#57a1f8", height=40)
            header_frame.pack(fill=tk.X)
            self.ctk_widgets.append(header_frame)  # Thêm vào list
        except Exception as e:
            print(f"Lỗi tạo CTk frames: {e}")
            # Fallback to regular tkinter frames
            table_container = tk.Frame(self, bg="white", relief="solid", bd=1)
            table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            
            header_frame = tk.Frame(table_container, bg="#57a1f8", height=40)
            header_frame.pack(fill=tk.X)

        headers = ["Tên đăng nhập", "Mật khẩu", "Email", "Số điện thoại", "Thao tác"]
        header_widths = [180, 160, 250, 150, 200]

        for i, width in enumerate(header_widths):
            header_frame.grid_columnconfigure(i, weight=0, minsize=width)

        for i, header in enumerate(headers):
            label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"),
                             bg="#57a1f8", fg="white", anchor="center")
            label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

        # Scrollable area
        scroll_container = tk.Frame(table_container, bg="white")
        scroll_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(scroll_container, bg="white")
        
        try:
            scrollbar = ctk.CTkScrollbar(master=scroll_container, orientation="vertical", command=self.canvas.yview,
                                     width=12, corner_radius=6,
                                     fg_color="white", bg_color="white",
                                     button_color="#57a1f8", button_hover_color="#2b8ee0")
            self.ctk_widgets.append(scrollbar)  # Thêm vào list
        except Exception as e:
            print(f"Lỗi tạo CTk scrollbar: {e}")
            # Fallback to regular tkinter scrollbar
            scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
            
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        try:
            self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="white")
            self.ctk_widgets.append(self.scrollable_frame)  # Thêm vào list
        except Exception as e:
            print(f"Lỗi tạo CTk scrollable frame: {e}")
            # Fallback to regular tkinter frame
            self.scrollable_frame = tk.Frame(self.canvas, bg="white")
            
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Bind mousewheel to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Load and display data
        self.refresh_data()

    def refresh_data(self):
        """Refresh the account data display"""
        self.load_data_account_from_file()
        
        # Clear existing data rows safely
        if self.scrollable_frame:
            for widget in self.scrollable_frame.winfo_children():
                try:
                    widget.destroy()
                except:
                    pass

        header_widths = [180, 160, 250, 150, 200]

        for i, account in enumerate(self.account_data):
            bg_color = "#f8f9fa" if i % 2 == 1 else "white"
            hover_color = "#d0e6ff"

            row_frame = tk.Frame(self.scrollable_frame, bg=bg_color, height=45)
            row_frame.pack(fill=tk.X)

            for j, width in enumerate(header_widths):
                row_frame.grid_columnconfigure(j, weight=0, minsize=width)

            display_data = [
                account.get('username', ''),
                '********' if 'password_hash' in account and account.get('password_hash') else '',
                account.get('email', ''),
                account.get('phone', '')
            ]

            for j, text in enumerate(display_data):
                label = tk.Label(row_frame, text=text, font=("Arial", 11),
                                 bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")

            # Action buttons
            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=4, padx=5, pady=5)

            try:
                detail_btn = ctk.CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                       fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                       corner_radius=3, font=("Arial", 9),
                                       command=lambda acc=account: self.view_account_detail(acc))
                detail_btn.pack(side=tk.LEFT, padx=2)

                edit_btn = ctk.CTkButton(master=action_frame, text="Sửa", width=50, height=28,
                                     fg_color="#ffc107", text_color="white", hover_color="#e0a800",
                                     corner_radius=3, font=("Arial", 9),
                                     command=lambda acc=account: self.edit_account(acc))
                edit_btn.pack(side=tk.LEFT, padx=2)

                delete_btn = ctk.CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                       fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                       corner_radius=3, font=("Arial", 9),
                                       command=lambda acc=account: self.delete_account(acc))
                delete_btn.pack(side=tk.LEFT, padx=2)
            except Exception as e:
                print(f"Lỗi tạo CTk action buttons: {e}")
                # Fallback to regular tkinter buttons
                detail_btn = tk.Button(action_frame, text="Chi tiết", bg="#17a2b8", fg="white",
                                     command=lambda acc=account: self.view_account_detail(acc))
                detail_btn.pack(side=tk.LEFT, padx=2)

                edit_btn = tk.Button(action_frame, text="Sửa", bg="#ffc107", fg="white",
                                   command=lambda acc=account: self.edit_account(acc))
                edit_btn.pack(side=tk.LEFT, padx=2)

                delete_btn = tk.Button(action_frame, text="Xóa", bg="#dc3545", fg="white",
                                     command=lambda acc=account: self.delete_account(acc))
                delete_btn.pack(side=tk.LEFT, padx=2)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if self.canvas:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_new_account(self):
        """Add new account - placeholder method"""
        messagebox.showinfo("Thông báo", "Chức năng thêm tài khoản sẽ được phát triển")

    def export_json(self):
        """Export account data to JSON file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Lưu file JSON"
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.account_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file: {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def view_account_detail(self, account):
        """View account details - placeholder method"""
        messagebox.showinfo("Chi tiết tài khoản", 
                           f"Tên đăng nhập: {account.get('username', '')}\n"
                           f"Email: {account.get('email', '')}\n"
                           f"Số điện thoại: {account.get('phone', '')}")

    def edit_account(self, account):
        """Edit account - placeholder method"""
        messagebox.showinfo("Thông báo", f"Chỉnh sửa tài khoản: {account.get('username', '')}")

    def delete_account(self, account):
        """Delete account"""
        result = messagebox.askyesno("Xác nhận", 
                                   f"Bạn có chắc chắn muốn xóa tài khoản '{account.get('username', '')}'?")
        if result:
            try:
                self.account_data.remove(account)
                self.save_data_account_to_file()
                self.refresh_data()
                messagebox.showinfo("Thành công", "Đã xóa tài khoản thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa tài khoản: {str(e)}")

    def destroy(self):
        """Override destroy method to safely clean up"""
        try:
            self.safe_destroy_widgets()
            super().destroy()
        except:
            pass
