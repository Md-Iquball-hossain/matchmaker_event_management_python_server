
# Author: Md. Iquball Hossain
# Date: 23-11-2023
# */

from flask import Blueprint
from app.database import conn
from app.auth.validators.vendor_validation import vendor_Validator
# from utils.decorator.input_validator import validate_form_data
from app.auth.services.auth_vendor_service import signup_vendor, login_vendor

auth_vendor = Blueprint("auth_vendor", __name__)


@auth_vendor.route("/sign-up", methods=["POST"])
# @validate_form_data(schema=vendor_Validator)
def signup():
    return signup_vendor()

@auth_vendor.route("/log-in", methods=["POST"])
def login():
    return login_vendor()