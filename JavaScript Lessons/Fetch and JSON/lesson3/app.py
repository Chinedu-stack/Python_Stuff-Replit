from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.get_json()

    print(f"Task: {data["task"]}")
    print()
    print()
    print("Nedu this is actually working!!!😊🤣😂")

    return jsonify({
        "message":"Task recieved",
        "task": data["task"]
    })



if __name__ == "__main__":
    app.run(debug=True)