from flask import Blueprint, jsonify, render_template, session, request
import json
import utils.helpers as helpers
from datetime import datetime, date

api_bp = Blueprint('api', __name__)

@api_bp.route("/fetch_tasks", methods=["GET"])
def dashboard():
    current_user = session.get("current_user")     
    user_id = helpers.get_user_id(current_user)

    tasks = helpers.display_all_tasks(user_id)
    return jsonify(tasks)


@api_bp.route("add_tasks", methods=["POST"])
def add_task():
    json_task = request.get_json()
    task = json.loads(json_task)
    current_user = session.get("current_user")
    user_id = helpers.get_user_id(current_user)
    task_name = task["task"]
    start_date = task["start_date"]
    end_date = task["end_date"]

    helpers.add_task(user_id, task_name, start_date, end_date)

