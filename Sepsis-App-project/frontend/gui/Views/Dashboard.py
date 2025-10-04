import customtkinter as ctk
from gui.Components.Base_DB_Component import DashBoardComponent

class DashBoardForm(ctk.CTk):
    def __init__(self):
        super().__init__()
        #setting background windows
        self.minsize(1062,600)
        self.center_desktop(1062,600)
        self._set_appearance_mode("System")  # or "Light", "Dark"
        self.title("Dash Board Hệ Thống Dự Báo Nhiễm Trùng Huyết")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.Component = DashBoardComponent(master=self, controller=None)
        self.Component.grid(row=0, column=0, sticky="nsew")  #  Thêm grid cho frame

# ========== CENTER DESKTOP ==========
    def center_desktop(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate coordinates for centering
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
