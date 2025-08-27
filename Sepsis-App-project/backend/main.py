# backend/main.py
from dotenv import load_dotenv
import os
# Tải biến môi trường ngay tại đây, trước mọi thứ khác
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Phần debug URL map của bạn (Giữ nguyên, rất hữu ích!)
    with app.app_context():
        print("\n===== Registered Routes =====")
        for rule in app.url_map.iter_rules():
            if rule.endpoint not in ['static']:
                print(f"Endpoint: {rule.endpoint}, Methods: {', '.join(rule.methods)}, Rule: {rule.rule}")
        print("=============================\n")
    
    # Sửa lỗi: Ép buộc server chạy ở chế độ debug để đảm bảo reloader hoạt động
    app.run(debug=True, port=5000)
