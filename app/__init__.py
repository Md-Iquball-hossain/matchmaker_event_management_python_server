from flask import Flask
from flask_cors import CORS
from app.router import app_router
from config import EMAIL_ID, EMAIL_PASSWORD

app = Flask(__name__)

# Initialize CORS with your app
CORS(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = EMAIL_ID
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD

@app.route("/")
def init_func():
    return "Match 360 Server is running."


def create_app():
    app.register_blueprint(app_router, url_prefix="/api/v1")
    return app
