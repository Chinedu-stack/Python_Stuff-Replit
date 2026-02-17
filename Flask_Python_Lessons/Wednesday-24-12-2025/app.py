from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("questionaire_form.html")

@app.route("/post_form/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Get data from POST form
        name = request.form.get("name", "No name given")
        age = request.form.get("age", "No age given")
        
        if not name or not age:
            error = "Please fill in both Name and Age!"
            return render_template("post_form.html", error=error)
        else:
            return render_template("result.html", name=name, age=age)
    else:
        # Show the form if accessed via GET 
        return render_template("post_form.html")



@app.route("/processing/", methods=["GET", "POST"])
def process():
    if request.method == "POST":
        name = request.form.get("name", "none given")
        food = request.form.get("food", "no food given")
        color = request.form.get("color", "no color given")
        coding_list = [name,food,color]

        if not name or not food or not color:
            error = "Please fill out all of the fields"
            return render_template("questionaire_form.html", error=error)
        else:
            return render_template("questionaire_results.html", coding_list=coding_list)
    else:
        return render_template("questionaire_form.html")


if __name__ == "__main__":
    app.run(debug=True)
