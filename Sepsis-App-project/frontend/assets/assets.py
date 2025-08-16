import os
from pathlib import Path

class AssetManager:
        BASE_DIR = Path(__file__).resolve().parent

        images = {
                #Dùng cho form đăng nhập
                "SignIn_Pic" : BASE_DIR / "images" / "SignIn_Pic.png",
        }

        @classmethod
        def get_image_path(cls,name):
            return cls.images.get(name)