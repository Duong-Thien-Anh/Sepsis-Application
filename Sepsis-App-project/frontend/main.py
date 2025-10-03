# main.py
from gui.Views.SignIn import SignInForm
from gui.Views.Dashboard import DashBoardForm

class MainApp:
    def __init__(self):
        self.app = SignInForm()

def run():
    main_app = MainApp()
    return main_app.app, main_app

if __name__ == "__main__":
    root, app = run()
    root.mainloop()

