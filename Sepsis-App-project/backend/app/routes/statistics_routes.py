from flask import Blueprint, jsonify
from app.services.statistics_service import get_gender_stats, get_age_group_stats

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/gender", methods=["GET"])
def gender_stats():
    return jsonify(get_gender_stats())

@stats_bp.route("/age-groups", methods=["GET"])
def age_group_stats():
    return jsonify(get_age_group_stats())
