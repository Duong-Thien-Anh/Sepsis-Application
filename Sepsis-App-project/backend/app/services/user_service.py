from app.models.models import User
from app.extensions import db
from sqlalchemy import or_

def get_all_users(args):
    query = User.query
    
    # Lọc theo vai trò
    role = args.get('role')
    if role:
        query = query.filter(User.role == role)
        
    # Tìm kiếm
    search_term = args.get('search')
    if search_term:
        query = query.filter(or_(
            User.username.ilike(f'%{search_term}%'),
            User.name.ilike(f'%{search_term}%'),
            User.email.ilike(f'%{search_term}%')
        ))
    return query.all()

def update_user_info(user, data):
    # Cập nhật logic để xử lý các trường mới
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return None, "Email đã được sử dụng.", 409
        user.email = data['email']
    
    if 'name' in data: user.name = data['name']
    if 'phone' in data: user.phone = data['phone']
    if 'role' in data: user.role = data['role']
    if 'is_active' in data: user.is_active = data['is_active']
    
    # Thêm chức năng đặt lại mật khẩu cho Admin
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    db.session.commit()
    return user, "Cập nhật thành công.", 200

def delete_user_by_id(user):
    db.session.delete(user)
    db.session.commit()
    return True, "Xóa người dùng thành công.", 200