import customtkinter as ctk

class PatientDialogs:
    """Class chứa các dialog xác nhận và cảnh báo."""
    
    def __init__(self, parent):
        """
        Args:
            parent: Component cha (Patient_UI)
        """
        self.parent = parent
    
    # ==================== CONFIRMATION POPUPS ====================
    
    def show_confirm_delete_popup(self, patient_name, on_confirm_callback):
        """Hiển thị popup xác nhận xóa bệnh nhân.
        
        Args:
            patient_name (str): Tên bệnh nhân
            on_confirm_callback: Callback(popup) khi nhấn Yes
        """
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Xác nhận xóa")
        popup.geometry("400x180")
        popup.resizable(False, False)
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (400 // 2)
        y = (popup.winfo_screenheight() // 2) - (180 // 2)
        popup.geometry(f"400x180+{x}+{y}")
        
        # Nội dung popup
        message = f"Bạn có chắc muốn xóa bệnh nhân\n'{patient_name}' không?"
        label = ctk.CTkLabel(
            popup,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        label.pack(pady=30)
        
        # Frame chứa 2 nút Yes/No
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=10)
        
        # Nút Yes
        yes_button = ctk.CTkButton(
            button_frame,
            text="Yes",
            width=100,
            height=35,
            fg_color="#F44336",
            hover_color="#da190b",
            command=lambda: on_confirm_callback(popup)
        )
        yes_button.pack(side="left", padx=10)
        
        # Nút No
        no_button = ctk.CTkButton(
            button_frame,
            text="No",
            width=100,
            height=35,
            fg_color="#66B7FF",
            hover_color="#45a049",
            command=popup.destroy
        )
        no_button.pack(side="left", padx=10)
    
    # ==================== WARNING POPUP ====================
    
    def show_warning_popup(self, message):
        """Hiển thị popup cảnh báo.
        
        Args:
            message (str): Nội dung cảnh báo
        """
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Cảnh báo")
        popup.geometry("300x150")
        popup.resizable(False, False)
        
        # Đưa popup lên trên cùng
        popup.lift()
        popup.attributes('-topmost', True)
        
        # Căn giữa màn hình
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (300 // 2)
        y = (popup.winfo_screenheight() // 2) - (150 // 2)
        popup.geometry(f"300x150+{x}+{y}")
        
        # Nội dung popup
        label = ctk.CTkLabel(
            popup,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=250
        )
        label.pack(pady=30)
        
        # Nút OK
        ok_button = ctk.CTkButton(
            popup,
            text="OK",
            width=100,
            height=35,
            fg_color="#66B7FF",
            hover_color="#45a049",
            command=popup.destroy
        )
        ok_button.pack(pady=10)
