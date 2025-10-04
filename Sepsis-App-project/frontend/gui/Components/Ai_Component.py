import customtkinter as ctk
from matplotlib.figure import Figure
from PIL import Image , ImageTk , ImageDraw, ImageOps
from assets.Assets_Management import AssetManager

class AI_UI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="red" , corner_radius=15)
        self.pack(fill="both", expand=True)