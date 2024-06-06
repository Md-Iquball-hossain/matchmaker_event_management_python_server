from functools import wraps
from flask import make_response, request
from utils.miscellaneous.status_code import status_code
from utils.miscellaneous.response_message import status_message
from functools import wraps

def validate_input_data(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validated_data = schema().load(request.get_json())
                req = validated_data
                return func(req, *args, **kwargs)
            except Exception as e:
                print(str(e))
                return make_response(
                    {'success': False, 'message': status_message['HTTP_UNPROCESSABLE_ENTITY']}, status_code['HTTP_UNPROCESSABLE_ENTITY'])
        return wrapper
    return decorator

def validate_form_data(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validated_data = schema().load(request.form)
                req = validated_data
                return func(req, *args, **kwargs)
            except Exception as e:
                print(str(e))
                return make_response(
                    {'success': False, 'message': status_message['HTTP_UNPROCESSABLE_ENTITY']}, status_code['HTTP_UNPROCESSABLE_ENTITY'])
        return wrapper
    return decorator

def sanitize_data(data):
    if 'field1' in data:
        data['field1'] = data['field1'].strip()
    return data
