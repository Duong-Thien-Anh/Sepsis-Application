import os

def create_file(path, content=""):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def create_structure(base_path):
    folders = {
        "backend": ["controller", "model", "view", "ai"],
        "frontend": ["controller", "model", "view"]
    }

    for module, subdirs in folders.items():
        module_path = os.path.join(base_path, module)
        os.makedirs(module_path, exist_ok=True)
        create_file(os.path.join(module_path, "requirements.txt"))

        for sub in subdirs:
            sub_path = os.path.join(module_path, sub)
            os.makedirs(sub_path, exist_ok=True)
            create_file(os.path.join(sub_path, "__init__.py"))

        # Tạo file chính
        main_file = "app.py" if module == "backend" else "main.py"
        create_file(os.path.join(module_path, main_file), f"# Entry point for {module}")

    # Tạo thêm assets/img cho frontend
    frontend_img_path = os.path.join(base_path, "frontend", "assets", "img")
    os.makedirs(frontend_img_path, exist_ok=True)

    # Tạo README và .gitignore gốc
    create_file(os.path.join(base_path, "README.md"), "# Python Desktop App - MVC Structure")
    create_file(os.path.join(base_path, ".gitignore"), "venv/\n__pycache__/\n*.pyc\n")

    print("Cấu trúc thư mục MVC đã được tạo thành công!")

if __name__ == "__main__":
    project_name = "desktop_app_mvc"
    create_structure(project_name)
