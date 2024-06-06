# Author: Shidul Islam
# Date: 07-11-2023
# */


from flask import Blueprint
from app.external.validators.external_validator import SendOTPSchema, MatchOTPSchema
from utils.decorator.input_validator import validate_input_data
from app.external.services.external_service import send_otp_service, match_otp_service


external = Blueprint('external_router', __name__)

# Send otp router


@external.post('/send-otp')
@validate_input_data(SendOTPSchema)
def send_otp(req):
    return send_otp_service(req)

# match otp router


@external.post('/match-otp')
@validate_input_data(MatchOTPSchema)
def match_otp(req):
    return match_otp_service(req)
