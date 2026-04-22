from flask import Flask
from routes.auth import auth_bp
from routes.api import api_bp

app = Flask(__name__)

app.secret_key = "Chinedu's_Key"

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run()