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


@api_bp.route("/add_tasks", methods=["POST"])
def add_task():
    task = request.get_json()
    current_user = session.get("current_user")
    user_id = helpers.get_user_id(current_user)
    task_name = task["task"]
    start_date = task["start_date"]
    end_date = task["end_date"]

    helpers.add_task(user_id, task_name, start_date, end_date)
    print("task added")
    return jsonify({"success":True})


@api_bp.route("/delete_tasks", methods=["POST"])
def delete_task():
    data = request.get_json()
    task_name = data["task"]
    current_user = session.get("current_user")
    user_id = helpers.get_user_id(current_user)
    task_id = helpers.get_task_id(user_id, task_name)
    
    helpers.delete_task(user_id, task_id)
    print("Task deleted")
    return jsonify({"success":True})


@api_bp.route("/edit_task", methods=["POST"])
def edit_task():
    data = request.get_json()
    current_user = session.get("current_user")
    user_id = helpers.get_user_id(current_user)
    task = data["task"]
    task_id = helpers.get_task_id(user_id, task)
    new_task = data["new_task"]

    helpers.edit_task(new_task, user_id, task_id)
    print("task edited")
    return jsonify({"success": True})


@api_bp.route("/task_done", methods=["POST"])
def mark_done():
    data = request.get_json()
    current_user = session.get("current_user")
    user_id = helpers.get_user_id(current_user)
    task = data["task"]
    task_id = helpers.get_task_id(user_id, task)

    helpers.mark_task_done(user_id, task_id)
    print("task marked as done")
    return jsonify({"success": True})
