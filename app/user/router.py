# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint
from app.user.routes.profile_routes import profile_router
from app.user.routes.preference_routes import user_preference
from app.user.routes.my_matches_routes import my_matches
from app.user.routes.recent_viewed_routes import recent_view_router
from app.user.routes.add_list_routes import add_list
from app.user.routes.user_service_route import user_service_routes


user = Blueprint("user", __name__)

user.register_blueprint(profile_router, url_prefix="/")
user.register_blueprint(user_preference, url_prefix="/")
user.register_blueprint(my_matches, url_prefix="/")
user.register_blueprint(recent_view_router, url_prefix="/")
user.register_blueprint(add_list, url_prefix="/")
user.register_blueprint(user_service_routes, url_prefix="/")
