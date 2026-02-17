from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("form.html")


@app.route("/list/", methods=["POST"])
def results():
  number=0
  food = request.form.getlist("food")
  clean_food = []
  for item in food:
    stripped = item.strip()
    if stripped != "":
        clean_food.append(stripped)
        number+=1


  return render_template("result.html", clean_food=clean_food, number=number)



if __name__ == "__main__":
    app.run(debug=True)

