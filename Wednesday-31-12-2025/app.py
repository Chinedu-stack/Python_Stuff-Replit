from flask import Flask, render_template, request

app = Flask(__name__)

# Global dictionary to store animals
animals = {}

@app.route("/")
def home():
    return render_template("form.html", animals=animals)

@app.route("/animals/", methods=["POST"])
def homeless():
    animal = request.form.get("Animal").strip()
    sound = request.form.get("Sound").strip()
    if animal and sound:
        animals[animal] = sound
    return render_template("form.html", animals=animals)

if __name__ == '__main__':
    app.run(debug=True)
