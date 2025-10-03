from flask import request, jsonify
from ..services import patient_service
from ..services.patient_service import get_patient_list, get_patient_by_id, delete_patient_by_id

def search_patient():
    data = request.get_json()
    patient_id = data.get("patient_id")
    if not patient_id:
        return jsonify({"error": "Vui lòng nhập mã bệnh nhân"}), 400

    patient_data = patient_service.find_patient_by_id(patient_id)
    if patient_data:
        return jsonify(patient_data)
    return jsonify({"message": "Không tìm thấy bệnh nhân"}), 404

def create_or_update_patient():
    data = request.get_json()
    status = patient_service.save_or_update_patient(data)
    if status == "updated":
        return jsonify({"message": "Cập nhật thông tin thành công"})
    else:
        return jsonify({"message": "Thêm mới bệnh nhân thành công"}), 201

def get_patients():
    # Lấy các tham số từ query string
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search = request.args.get("search", "", type=str)
    gender = request.args.get("gender", None, type=str)

    # Gọi service để lấy danh sách bệnh nhân
    result = get_patient_list(page, per_page, search, gender)
    return jsonify(result)

def get_patient_detail(patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        return jsonify({"error": "Bệnh nhân không tồn tại"}), 404
    return jsonify(patient)

def delete_patient(patient_id):
    success = delete_patient_by_id(patient_id)
    if not success:
        return jsonify({"error": "Bệnh nhân không tồn tại"}), 404
    return jsonify({"message": "Xóa bệnh nhân thành công"})
