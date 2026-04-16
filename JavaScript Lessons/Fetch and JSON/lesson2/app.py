from flask import Flask, request, jsonify

app = Flask(__name__)



@app.route("/add-user", methods=["POST"])
def add_user():
    data = request.get_json()
    return jsonify({"status": "ye its all good broski",
                    "name":data["name"],
                    "age":data["age"]}
                   )