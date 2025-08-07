import os

def create_project_structure(project_name):
    # Cấu trúc các thư mục
    folders = [
        f"{project_name}/backend/app/controllers",
        f"{project_name}/backend/app/models",
        f"{project_name}/backend/app/routes",
        f"{project_name}/backend/app/services",
        f"{project_name}/frontend/gui",
        f"{project_name}/frontend/controllers",
        f"{project_name}/frontend/assets"
    ]

    # Các file mặc định
    files = {
        f"{project_name}/backend/main.py": "# Flask hoặc FastAPI entry point\n",
        f"{project_name}/backend/requirements.txt": "# Flask==2.x hoặc FastAPI\n",
        f"{project_name}/frontend/main.py": "# Chạy giao diện tkinter hoặc customtkinter\n",
        f"{project_name}/frontend/requirements.txt": "# tkinter hoặc customtkinter\n",
        f"{project_name}/README.md": f"# Dự án {project_name}\n\nMô tả dự án ứng dụng desktop tách FE và BE."
    }

    # Tạo thư mục
    print(f"\n📁 Đang tạo cấu trúc cho dự án: {project_name}\n")
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"📂 Đã tạo thư mục: {folder}")

    # Tạo file
    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Đã tạo file: {file_path}")

    print("\n✅ Hoàn tất! Cấu trúc dự án đã được tạo thành công.\n")

# ================================
if __name__ == "__main__":
    project_name = input("📝 Nhập tên thư mục dự án (VD: sepsis-detector-app): ").strip()
    if project_name:
        create_project_structure(project_name)
    else:
        print("❌ Bạn chưa nhập tên dự án.")
