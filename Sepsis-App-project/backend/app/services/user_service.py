from app.models.models import db, User
from sqlalchemy import or_

def get_all_users(search_term):
    query = User.query
    if search_term:
        query = query.filter(or_(
            User.name.ilike(f'%{search_term}%'),
            User.email.ilike(f'%{search_term}%')
        ))
    return query.all()

def update_user_info(user, data):
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return None, "Email đã được sử dụng.", 409
        user.email = data['email']
    
    if 'name' in data: user.name = data['name']
    if 'is_admin' in data: user.is_admin = data['is_admin']
    if 'is_active' in data: user.is_active = data['is_active']
    
    db.session.commit()
    return user, "Cập nhật thành công.", 200

def delete_user_by_id(user):
    db.session.delete(user)
    db.session.commit()
    return True, "Xóa người dùng thành công.", 200