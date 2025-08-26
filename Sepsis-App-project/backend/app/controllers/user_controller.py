# backend/app/controllers/user_controller.py
from flask import request, jsonify
from app.services import user_service
from app.models.models import User

def get_users():
    search_term = request.args.get('search')
    users = user_service.get_all_users(search_term)
    return jsonify([user.to_dict() for user in users]), 200

def update_user(user_id):
    user = User.query.get_or_404(user_id)
    updated_user, message, status_code = user_service.update_user_info(user, request.get_json())
    if not updated_user: return jsonify({"message": message}), status_code
    return jsonify(updated_user.to_dict()), status_code

def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    success, message, status_code = user_service.delete_user_by_id(user)
    return jsonify({"message": message}), status_code