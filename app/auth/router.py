from flask import Blueprint
from app.auth.routes.auth_routes import auth_router


auth = Blueprint("auth", __name__)

auth.register_blueprint(auth_router, url_prefix="/")
