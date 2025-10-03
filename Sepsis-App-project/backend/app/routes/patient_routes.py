from flask import Blueprint
from ..controllers import patient_controller as controller

patient_bp = Blueprint("patient_bp", __name__)

patient_bp.route("/search", methods=["POST"])(controller.search_patient)
patient_bp.route("/save", methods=["POST"])(controller.create_or_update_patient)
patient_bp.route("/list", methods=["GET"])(controller.get_patients)
patient_bp.route("/<string:patient_id>", methods=["GET"])(controller.get_patient_detail)
patient_bp.route("/<string:patient_id>", methods=["DELETE"])(controller.delete_patient)
