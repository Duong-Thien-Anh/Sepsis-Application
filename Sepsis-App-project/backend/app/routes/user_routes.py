# backend/app/routes/user_routes.py
from flask import Blueprint
from app.controllers import user_controller
from app.auth.decorators import admin_required # Tạo file decorator mới

user_bp = Blueprint('users', __name__)

user_bp.route('/', methods=['GET'])(admin_required()(user_controller.get_users))
user_bp.route('/<int:user_id>', methods=['PUT'])(admin_required()(user_controller.update_user))
user_bp.route('/<int:user_id>', methods=['DELETE'])(admin_required()(user_controller.delete_user))