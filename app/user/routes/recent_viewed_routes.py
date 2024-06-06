# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint
from app.database import conn
from app.user.services.recent_viewed_service import recent_view_data, get_recent_view_data, get_visitor
# from utils.decorator.input_validator import validate_input_data, validate_form_data
from utils.decorator.auth_checker import user_token_authentication
from app.user.validators.update_profile_validator import UpdateProfileValidator
recent_view_router = Blueprint("recent_view", __name__)

@recent_view_router.route("/recent-view", methods=["POST"])
@user_token_authentication()
def recent_view(current_user):
    return recent_view_data(current_user)

@recent_view_router.route("/get-recent-view", methods=["GET"])
@user_token_authentication()
def get_recent_view(current_user):
    return get_recent_view_data(current_user)

@recent_view_router.route("/get-recent-visitor", methods=["GET"])
@user_token_authentication()
def get_recent_visitor(current_user):
    return get_visitor(current_user)
