from flask import Blueprint, jsonify, render_template, session
import json
import utils.helpers as helpers
from datetime import datetime, date

api_bp = Blueprint('api', __name__)

@api_bp.route("/api_fetch_dashboard", methods=["GET"])
def dashboard():
    date_today = date.today()
    day = date_today.strftime("%A")
    today = datetime.today().strftime("%Y-%m-%d")

    current_user = session.get("current_user")     
    user_id = helpers.get_user_id(current_user)

    tasks = helpers.display_tasks_day(user_id, today)
    return jsonify(tasks)

