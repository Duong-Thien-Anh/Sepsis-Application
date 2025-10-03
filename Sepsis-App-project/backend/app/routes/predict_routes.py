from flask import Blueprint
from ..controllers import predict_controller

predict_bp = Blueprint("predict_bp", __name__)

predict_bp.route("/predict", methods=["POST"])(predict_controller.predict)
