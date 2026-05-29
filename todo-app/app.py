from flask import Flask
from routes.auth import auth_bp
from routes.api import api_bp
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run()   