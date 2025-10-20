import customtkinter as ctk
from gui.Components.Base_Component import SignInComponent
from gui.Components.Base_DB_Component import DashBoardComponent

class Frame_DB(ctk.CTk):
    """
    Cửa sổ chính của ứng dụng (CTk root window).
    Quản lý việc chuyển đổi giữa các màn hình (CTkFrame components).
    
    Flow:
    1. Khởi tạo → Hiển thị SignInComponent (đăng nhập)
    2. Đăng nhập thành công → Chuyển sang DashBoardComponent
    3. Logout → Quay lại SignInComponent
    """
    def __init__(self, master=None):
        super().__init__(master)
        
        # Setting background windows
        self.minsize(1062, 600)
        self.center_desktop(1062, 600)
        self._set_appearance_mode("System")
        self.title("Hệ Thống Dự Báo Nhiễm Trùng Huyết")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Container để chứa các component (frame)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        
        # Khởi tạo các component (chưa hiển thị)
        self.current_component = None
        self.signin_component = None
        self.dashboard_component = None
        
        # Hiển thị màn hình đăng nhập đầu tiên
        self.show_signin()

    def show_signin(self):
        """Hiển thị màn hình đăng nhập (SignInComponent)."""
        # Ẩn component hiện tại
        if self.current_component:
            self.current_component.grid_forget()
        
        # Tạo SignInComponent nếu chưa có (hoặc reuse nếu đã có)
        if self.signin_component is None:
            from controllers.Login_Controller import LoginController
            controller = LoginController()
            self.signin_component = SignInComponent(
                master=self.container,
                controller=controller,
                parent_window=self  # Truyền reference để gọi show_dashboard()
            )
        
        # Hiển thị SignIn
        self.signin_component.grid(row=0, column=0, sticky="nsew")
        self.current_component = self.signin_component
        
        # Resize window cho phù hợp với SignIn
        self.geometry("862x500")
        self.center_desktop(862, 500)
        self.title("Đăng nhập hệ thống")
        print("✅ Đang hiển thị màn hình đăng nhập")

    def show_dashboard(self):
        """Hiển thị màn hình chính (DashBoardComponent) sau khi đăng nhập thành công."""
        # Ẩn SignIn component
        if self.current_component:
            self.current_component.grid_forget()
        
        # Hủy SignIn component để giải phóng bộ nhớ (optional)
        if self.signin_component:
            self.signin_component.destroy()
            self.signin_component = None
        
        # Tạo DashBoard component nếu chưa có
        if self.dashboard_component is None:
            self.dashboard_component = DashBoardComponent(
                master=self.container,
                parent_window=self  # Truyền reference để logout
            )
        
        # Hiển thị Dashboard
        self.dashboard_component.grid(row=0, column=0, sticky="nsew")
        self.current_component = self.dashboard_component
        
        # Resize window cho phù hợp với Dashboard
        self.geometry("1062x600")
        self.center_desktop(1062, 600)
        self.title("Dash Board Hệ Thống Dự Báo Nhiễm Trùng Huyết")
        print("✅ Đang hiển thị màn hình chính (Dashboard)")

    def logout(self):
        """Đăng xuất - quay về màn hình đăng nhập."""
        # Ẩn Dashboard component
        if self.current_component:
            self.current_component.grid_forget()
        
        # Hủy Dashboard để giải phóng bộ nhớ (optional)
        if self.dashboard_component:
            self.dashboard_component.destroy()
            self.dashboard_component = None
        
        # Hiển thị lại SignIn
        self.show_signin()
        print("✅ Đã đăng xuất, quay về màn hình đăng nhập")

    # ========== CENTER DESKTOP ==========
    def center_desktop(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate coordinates for centering
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
