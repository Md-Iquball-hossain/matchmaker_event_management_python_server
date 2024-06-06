# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint
from app.database import conn
from app.user.services.preference_service import user_preference_data, user_preference_update
from utils.decorator.auth_checker import user_token_authentication
user_preference = Blueprint("preference", __name__)


@user_preference.route("/user_preference", methods=["GET"])
@user_token_authentication()
def preference(current_user):
    return user_preference_data(current_user)


@user_preference.route("/user_preference", methods=["PUT"])
@user_token_authentication()
def preference_update(current_user):
    return user_preference_update(current_user)
