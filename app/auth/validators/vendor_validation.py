# Author: Md. Iquball Hossain <iquball.m360ict@gmail.com>
# Date: 23-11-2023
# */
from marshmallow import Schema, fields

class vendor_Validator(Schema):
    org_name = fields.String(required=True, error_messages={
        "required": {"message": "organizationname is required"}})
    org_username = fields.Str(required=True, error_messages={
        "required": {"message": "username is required"}})
    email = fields.String(required=True, error_messages={
        "required": {"message": "email is required"}})
    password = fields.String(required=True, error_messages={
        "required": {"message": "password is required"}})
    phone_number = fields.String(required=True, error_messages={
        "required": {"message": "phone_number is required"}})
    city = fields.String(required=True, error_messages={
        "required": {"message": "city is required"}})
    country = fields.String(required=True, error_messages={
        "required": {"message": "country is required"}})
    business_category = fields.String(required=True, error_messages={
        "required": {"message": "education is required"}})