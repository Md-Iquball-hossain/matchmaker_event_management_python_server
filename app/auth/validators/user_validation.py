from marshmallow import Schema, fields, validate


class UserValidator(Schema):
    username = fields.Str(required=True, error_messages={
        "required": {"message": "username is required"}})
    email = fields.String(required=True, error_messages={
        "required": {"message": "email is required"}})
    password = fields.String(required=True, error_messages={
        "required": {"message": "password is required"}})
    phone_number = fields.String(required=True, error_messages={
        "required": {"message": "phone_number is required"}})
    date_of_birth = fields.String(required=True, error_messages={
        "required": {"message": "date_of_birth is required"}})
    religion = fields.String(required=True, error_messages={
        "required": {"message": "religion is required"}})
    community = fields.String(required=True, error_messages={
        "required": {"message": "community is required"}})
    country = fields.String(required=True, error_messages={
        "required": {"message": "country is required"}})
    gender = fields.String(required=True, error_messages={
        "required": {"message": "gender is required"}})
    education = fields.String(required=True, error_messages={
        "required": {"message": "education is required"}})
    occupation = fields.String(required=True, error_messages={
        "required": {"message": "occupation is required"}})
    about_me = fields.String(required=True, error_messages={
        "required": {"message": "about_me is required"}})
