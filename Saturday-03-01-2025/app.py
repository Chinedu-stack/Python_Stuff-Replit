from flask import Flask, render_template, request

app = Flask(__name__)

students = []

@app.route("/")
def home():
    return render_template("dashboard.html", students=students)

@app.route("/form/")
def homelessness():
    return render_template("form.html")


@app.route("/processing/", methods=["GET", "POST"])
def homeless():
    if request.method == "POST":
        dictionary = {}
        name = request.form.get("name")
        sport = request.form.get("sport")
        instrument = request.form.get("instrument")
        iq = request.form.get("iq")
        if iq.isdigit():
            iq = int(iq)
        else:
            iq = 0  # Default if empty or invalid
        dictionary["Name"] = name
        dictionary["Sport"] = sport
        dictionary["Instrument"] = instrument
        dictionary["iq"] = iq
        students.append(dictionary)
        return render_template("dashboard.html", students=students)
    else:
        return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)