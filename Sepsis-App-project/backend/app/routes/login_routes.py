from flask import Blueprint
from ..controllers import login_controller as controller

login_bp = Blueprint("login_bp", __name__)
login_bp.route("/login", methods=["POST"])(controller.login)
