from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

tasks = [
    {"id":1, "text":"football"},
    {"id":2, "text":"reading"}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/delete_task", methods=["POST"])
def delete_task():
    global tasks
    data = request.get_json()
    task_id = data["id"]
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)


