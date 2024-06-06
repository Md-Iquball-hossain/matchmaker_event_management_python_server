from marshmallow import Schema, fields, validate


class UserPreferenceValidator(Schema):
    from_age = fields.Number(required=True, error_messages={
        "required": {"message": "from_age is required"}})
    to_age = fields.Number(required=True, error_messages={
        "required": {"message": "to_age is required"}})
    desired_religion = fields.List(fields.String(required=True, error_messages={
        "required": {"message": "password is required"}}), validate=validate.Length(min=1))
    desired_country = fields.List(fields.String(required=True, error_messages={
        "required": {"message": "desired_country is required"}}, validate=validate.Length(min=1)))
    desired_community = fields.List(fields.String(required=True, error_messages={
        "required": {"message": "desired_community is required"}},  validate=validate.Length(min=1)))
    desired_occupation = fields.List(fields.String(required=True, error_messages={
        "required": {"message": "desired_occupation is required"}},  validate=validate.Length(min=1)))
    desired_education = fields.List(fields.String(required=True, error_messages={
        "required": {"message": "desired_education is required"}},  validate=validate.Length(min=1)))
    desired_language = fields.List(fields.String(required=True, error_messages={
        "required": {"message": "desired_language is required"}},  validate=validate.Length(min=1)))
    desired_marital_status = fields.List(fields.String(required=True, error_messages={
        "required": {"message": "desired_marital_status is required"}},  validate=validate.Length(min=1)))
    desired_gender = fields.List(fields.String(required=True, error_messages={
        "required": {"message": "desired_gender is required"}},  validate=validate.Length(min=1)))
