#----------------------------------  Topics : vendor profile update validation, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

from marshmallow import Schema, fields, validate
class UpdateVendorProfileValidator(Schema):

    org_name = fields.Str(required=True, error_messages={
        "required": {"message": "Organization name is required."}})
    org_username = fields.Str(required=True, error_messages={
        "required": {"message": "Organization username is required."}})
    email = fields.Email(required=True, error_messages={
        "required": {"message": "Email is required."},
        "invalid": {"message": "Invalid email format."}})
    password = fields.String(required=True, error_messages={
        "required": {"message": "Password is required."}})
    phone_number = fields.String(required=True, error_messages={
        "required": {"message": "Phone number is required."}})
    photo = fields.String()
    address = fields.Str(required=True, error_messages={
        "required": {"message": "Address is required."}})
    city = fields.Str(validate=validate.OneOf(['Dhaka', 'YourEnumValuesHere']))
    country = fields.Str(validate=validate.OneOf(['Bangladesh', 'YourEnumValuesHere']))
    business_category = fields.Str(validate=validate.OneOf(['Food', 'YourEnumValuesHere']))
    details = fields.Str()


