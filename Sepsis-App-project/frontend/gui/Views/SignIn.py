import customtkinter as ctk
from gui.Components.SignIn_Component import center_desktop , outer_fr_signin, container_fr_signin, layer1_fr_signin, layer2_fr_signin

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



