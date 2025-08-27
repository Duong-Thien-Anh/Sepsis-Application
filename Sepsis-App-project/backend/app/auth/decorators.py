# backend/app/auth/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required():
    """
    Decorator để đảm bảo chỉ người dùng có claim role='Admin'
    mới có thể truy cập route.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            # Thêm "camera giám sát" để xem nội dung token
            print(f"--- DEBUG: CLAIMS IN TOKEN: {claims} ---")
            
            if claims.get("role") == "Admin":
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Yêu cầu quyền Admin!"), 403
        return decorator
    return wrapper