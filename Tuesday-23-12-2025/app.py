from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("profile_form.html")

@app.route("/result/")
def result():
    sport = request.args.get("sport", "So you don't play sports you flippin ai chatbot")
    number = request.args.get("number", "alright fair enough")
    color = request.args.get("color", "Brev just pick a color")
    return render_template("result.html", sport=sport, number=number,color=color)


@app.route("/profile/")
def form():
    return render_template("profile_form.html")




@app.route("/profile_result/")
def profile_results():
    name = request.args.get("name") or "No name given"
    age = request.args.get("age") or "No age given"
    sport = request.args.get("sport") or "No sport given"
    color = request.args.get("color") or "No color given"
    hobby = request.args.get("hobby") or "No hobby given"
    
    return render_template(
        "profile_result.html",
        name=name,
        age=age,
        sport=sport,
        color=color,
        hobby=hobby
    ) 



if __name__ == "__main__":
    app.run(debug=True)
