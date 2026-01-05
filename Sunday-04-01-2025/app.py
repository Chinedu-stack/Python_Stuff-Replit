from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/result/", methods=["GET", "POST"])
def something():
    if request.method == "POST":
        errors = []

        # Get inputs safely
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        hobbies = request.form.getlist("hobbies")

        if not hobbies:
            errors.append("Please select at least one hobby")
        #validate gender
        if not gender:
            errors.append("Please select a gender")
        # Validate name
        if not name:
            errors.append("Name is not filled out")

        # Validate age
        if not age.isdigit():
            errors.append("Age must be a number")
        else:
            age_int = int(age)
            if age_int < 1 or age_int > 100:
                errors.append("Age must be between 1 and 100")

        # If there are errors, show form again
        if errors:
            return render_template("form.html", errors=errors, name=name, age=age, gender=gender,hobbies=hobbies)
        else:
            return render_template("result.html", name=name, age=age_int, gender=gender, hobbies=hobbies)

    else:
        return render_template("form.html")



if __name__ == "__main__":
    app.run(debug=True)