from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/result/", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        errors = []
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        email = request.form.get("email", "").strip()

        # Name validations
        if name == "":
            errors.append("Name is not filled out")
        if len(name) < 5:
            errors.append("Name must be 5 or more characters")

        # Age validations
        if age == "":
            errors.append("Age is not filled out")
        elif not age.isdigit():
            errors.append("Age must be a number")
        else:
            age_num = int(age)
            if age_num < 13 or age_num > 18:
                errors.append("Age must be between 13 and 18")

        # Email validations
        if email == "":
            errors.append("Email is not filled out")
        elif "@" not in email or "." not in email:
            errors.append("Invalid email")
        elif len(email) < 5:
            errors.append("Email cannot be less that 5 characters")


        # Render form again if there are errors
        if errors:
            return render_template("form.html", errors=errors, name=name, age=age, email=email)
        # Otherwise show results
        else:
            return render_template("result.html", name=name, age=age, email=email)

    # If GET request
    else:
        return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
