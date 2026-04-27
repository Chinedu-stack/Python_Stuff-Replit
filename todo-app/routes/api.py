from flask import Blueprint, jsonify, render_template, session
import json
import utils.helpers as helpers
from datetime import datetime, date

api_bp = Blueprint('api', __name__)

@api_bp.route("/tasks", methods=["GET"])
def dashboard():
    current_user = session.get("current_user")     
    user_id = helpers.get_user_id(current_user)

    tasks = helpers.display_all_tasks(user_id)
    return jsonify(tasks)

