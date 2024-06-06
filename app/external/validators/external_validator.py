from marshmallow import Schema, validate, fields
from utils.miscellaneous.constants import VERIFY_ADMIN, VERIFY_USER, VERIFY_VENDOR


class SendOTPSchema(Schema):
    email = fields.Email(required=True, error_message={
        "required": {"message": "email is required"}
    })
    type = fields.String(required=True, validate=validate.OneOf(
        [VERIFY_ADMIN, VERIFY_USER, VERIFY_VENDOR]
    ))


class MatchOTPSchema(Schema):
    email = fields.Email(required=True, error_message={
        "required": {"message": "email is required"}
    })
    type = fields.String(required=True, validate=validate.OneOf(
        [VERIFY_ADMIN, VERIFY_USER, VERIFY_VENDOR]
    ))
    otp = fields.String(required=True)
