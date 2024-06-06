# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import make_response, request
import re, jwt
from functools import wraps
from utils.miscellaneous.status_code import status_code
from utils.miscellaneous.response_message import status_message
from config import USER_SECRET, VENDOR_SECRET, ADMIN_SECRET, SUPER_ADMIN_SECRET


def user_token_authentication():
    def inner1(func):
        @wraps(func)
        def inner2(*args, **kwargs):
            try:
                authorization = request.headers.get("authorization")
                if not re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    return make_response(
                        {'success': False, "message": status_message['HTTP_UNAUTHORIZED']}, status_code['HTTP_UNAUTHORIZED'])
                token = authorization.split(' ')[1]
                current_user = jwt.decode(
                    token, USER_SECRET, algorithms=["HS256"])
                if not current_user:
                    return make_response(
                        {'success': False, 'message': status_message['HTTP_UNAUTHORIZED']}, status_code['HTTP_UNAUTHORIZED'])
                return func(current_user, *args, **kwargs)
            except Exception as e:
                print(e)
                return make_response(
                    {'success': False, 'message': status_message['HTTP_UNAUTHORIZED']}, status_code['HTTP_UNAUTHORIZED'])
        return inner2
    return inner1

#----------------------------------  Topics : Vendor authorization decode and auth_checker, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

def vendor_token_authentication():
    def inner1(func):
        @wraps(func)
        def inner2(*args, **kwargs):
            try:
                authorization = request.headers.get("Authorization")
                if not re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    return make_response(
                        {'success': False, "message": status_message['HTTP_UNAUTHORIZED']}, status_code['HTTP_UNAUTHORIZED'])
                token = authorization.split(' ')[1]
                current_vendor = jwt.decode(
                    token, VENDOR_SECRET, algorithms=["HS256"])
                if not current_vendor:
                    return make_response(
                        {'success': False, 'message': status_message['HTTP_UNAUTHORIZED']}, status_code['HTTP_UNAUTHORIZED'])
                return func(current_vendor, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return make_response(
                    {'success': False, 'message': 'Token expired'}, status_code['HTTP_UNAUTHORIZED'])
            except jwt.InvalidTokenError:
                return make_response(
                    {'success': False, 'message': 'Invalid token'}, status_code['HTTP_UNAUTHORIZED'])
            except Exception as e:
                print("Token verification error:", e)
                return make_response(
                    {'success': False, 'message': 'Token verification failed'}, status_code['HTTP_UNAUTHORIZED'])
        return inner2
    return inner1

#----------------------------------  Topics : Vendor authorization decode and auth_checker, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

def admin_token_authentication():
    def inner1(func):
        @wraps(func)
        def inner2(*args, **kwargs):
            try:
                authorization = request.headers.get("Authorization")
                if not re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    return make_response(
                        {'success': False, "message": status_message['HTTP_UNAUTHORIZED']}, status_code['HTTP_UNAUTHORIZED'])
                token = authorization.split(' ')[1]
                current_admin = jwt.decode(
                    token, ADMIN_SECRET, algorithms=["HS256"])
                if not current_admin:
                    return make_response(
                        {'success': False, 'message': status_message['HTTP_UNAUTHORIZED']}, status_code['HTTP_UNAUTHORIZED'])
                return func(current_admin, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return make_response(
                    {'success': False, 'message': 'Token expired'}, status_code['HTTP_UNAUTHORIZED'])
            except jwt.InvalidTokenError:
                return make_response(
                    {'success': False, 'message': 'Invalid token'}, status_code['HTTP_UNAUTHORIZED'])
            except Exception as e:
                print("Token verification error:", e)
                return make_response(
                    {'success': False, 'message': 'Token verification failed'}, status_code['HTTP_UNAUTHORIZED'])
        return inner2
    return inner1
