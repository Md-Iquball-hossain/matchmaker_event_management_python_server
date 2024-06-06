# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint
from app.database import conn
from app.auth.validators.user_validation import UserValidator
from app.auth.validators.preference_validation import UserPreferenceValidator
from utils.decorator.input_validator import validate_input_data, validate_form_data
from app.auth.services.auth_user_service import signup_form, login_form, user_preference 

auth_router = Blueprint("auth", __name__)


@auth_router.route("/sign-up", methods=["POST"])
@validate_form_data(schema=UserValidator)
def signup(req):
    return signup_form(req)


@auth_router.route("/user-preference/sign-up", methods=["POST"])
@validate_input_data(schema=UserPreferenceValidator)
def user_preference_signup(req):
    return user_preference(req)


@auth_router.route("/login", methods=["POST"])
def login():
    return login_form()