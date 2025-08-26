from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required():
    """
    Decorator để đảm bảo chỉ người dùng có claim is_admin=True
    trong JWT mới có thể truy cập route.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Xác thực sự tồn tại của một JWT hợp lệ
            verify_jwt_in_request()
            # Lấy payload (nội dung) của JWT
            claims = get_jwt()
            # Kiểm tra xem claim 'is_admin' có tồn tại và bằng True không
            if claims.get("is_admin"):
                # Nếu đúng, cho phép request đi tiếp
                return fn(*args, **kwargs)
            else:
                # Nếu không, trả về lỗi 403 Forbidden
                return jsonify(msg="Yêu cầu quyền Admin!"), 403
        return decorator
    return wrapper