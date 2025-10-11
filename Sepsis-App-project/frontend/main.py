# main.py
from gui.Views.SignIn import SignInForm
from gui.Views.Dashboard import DashBoardForm

class MainApp:
    def __init__(self):
        # Do not create nested MainApp instances here. Create the GUI window instance.
        self.root = SignInForm()

    def run(self):
        """Start and return the GUI root and this MainApp instance."""
        return self.root, self

def main():
    app = MainApp()
    root, _ = app.run()
    root.mainloop()


if __name__ == "__main__":
    main()

