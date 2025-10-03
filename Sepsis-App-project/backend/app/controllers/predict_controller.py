from flask import request, jsonify
from ..services import predict_service

def predict():
    body = request.get_json()
    if not body:
        return jsonify({"error": "Không có dữ liệu"}), 400

    try:
        data = [
            float(body["prg"]),
            float(body["pl"]),
            float(body["pr"]),
            float(body["sk"]),
            float(body["ts"]),
            float(body["m11"]),
            float(body["bd2"]),
            int(body["age"]),
            int(body["insurance"])
        ]
    except (ValueError, KeyError) as e:
        return jsonify({"error": f"Dữ liệu không hợp lệ: {e}"}), 400

    result = predict_service.predict_sepsis(data)
    return jsonify(result)
