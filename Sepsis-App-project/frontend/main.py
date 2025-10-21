# main.py
from gui.Views.Windows_Dashboard import Windows_DB

class MainApp:
    def __init__(self):
        """
        Khởi tạo ứng dụng chính.
        Windows_DB là cửa sổ chính (CTk root window) chứa các component (CTkFrame).
        """
        self.root = Windows_DB()

    def run(self):
        """Start and return the GUI root and this MainApp instance."""
        return self.root, self

def main():
    """Entry point của ứng dụng."""
    app = MainApp()
    root, _ = app.run()
    root.mainloop()


if __name__ == "__main__":
    main()

