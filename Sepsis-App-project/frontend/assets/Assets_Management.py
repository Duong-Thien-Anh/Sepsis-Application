import os
from pathlib import Path

class AssetManager:
        BASE_DIR = Path(__file__).resolve().parent

        images = {
                #Dùng cho form đăng nhập
                "SignIn_Pic" : BASE_DIR / "images" / "SignIn_Pic.png",
                "Gmail_Icon" : BASE_DIR / "images" / "Gmail_Icon.png",
                "Title_Home" : BASE_DIR / "images" / "TitleHome_Pic.png",
                "Avatar_Default" : BASE_DIR / "images" / "Avatar_Default.png"

        }
        icons = {
                #Dùng cho icons
                "btn_Account"          : BASE_DIR / "icons" / "btn_Account.png",
                "btn_Ai"               : BASE_DIR / "icons" / "btn_Ai.png",
                "btn_Employee"         : BASE_DIR / "icons" / "btn_Employee.png",
                "btn_Menu"             : BASE_DIR / "icons" / "btn_Menu.png",
                "btn_Patient"          : BASE_DIR / "icons" / "btn_Patient.png",
                "btn_Recall_Appointment" : BASE_DIR / "icons" / "btn_Recall_Appointment.png",
                "btn_setting"          : BASE_DIR / "icons" / "btn_setting.png",
                "btn_Sign_Out"         : BASE_DIR / "icons" / "btn_Sign_Out.png",
                "btn_Notification"     : BASE_DIR / "icons" / "btn_Notification.png",
                "icon_Bell"            : BASE_DIR / "icons" / "icon_Bell.png",
                "badge_Red"            : BASE_DIR / "icons" / "badge_Red.png",
                "btn_Refresh"          : BASE_DIR / "icons" / "btn_Refresh.png"
        }

        @classmethod
        def get_image_path(cls,name):
            return cls.images.get(name)

        @classmethod
        def get_icon_path(cls,name):
            return cls.icons.get(name)