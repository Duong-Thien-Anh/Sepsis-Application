# backend/app/routes/auth_routes.py
from flask import Blueprint
from app.controllers import auth_controller
from flask_jwt_extended import jwt_required
from app.auth.decorators import admin_required

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register', methods=['POST'])(admin_required()(auth_controller.register))
auth_bp.route('/login', methods=['POST'])(auth_controller.login)
auth_bp.route('/google/login')(auth_controller.google_login)
auth_bp.route('/google/callback')(auth_controller.google_callback)
auth_bp.route('/me', methods=['GET'])(jwt_required()(auth_controller.get_me))
