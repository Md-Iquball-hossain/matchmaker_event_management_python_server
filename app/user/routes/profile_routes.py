# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint
from app.database import conn
from app.user.services.profile_service import get_profile, update_profile
# from utils.decorator.input_validator import validate_input_data, validate_form_data
from utils.decorator.auth_checker import user_token_authentication
from app.user.validators.update_profile_validator import UpdateProfileValidator
profile_router = Blueprint("profile", __name__)


@profile_router.route("/profile", methods=["GET"])
@user_token_authentication()
def profile(current_user):
    return get_profile(current_user)


@profile_router.route("/update/profile", methods=["PUT"])
# @validate_form_data(schema=UpdateProfileValidator)
@user_token_authentication()
def profile_update(current_user):
    return update_profile(current_user)
