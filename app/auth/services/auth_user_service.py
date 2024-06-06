# Author: Shidul Islam <shidul.m360ict@gmail.com>
# Date: 10-11-2023
# */

from flask import Blueprint, jsonify, request
from app.database import conn
from psycopg2 import sql
from config import USER_SECRET
from app.auth.utils.auth_user import user_preference_data, user_information_data
from utils.miscellaneous.status_code import status_code
from utils.s3_bucket.s3_bucket import Uploader
from utils.miscellaneous.response_message import status_message
from utils.lib.lib import hash_password, create_token, verify_password
auth_user_service = Blueprint("auth_service", __name__)

def signup_form(req):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        data = req
        file = request.files['photo'] if 'photo' in request.files else None
        if file:
            s3_bucket = Uploader.cloudUpload(file, "photo")
            user_information = user_information_data(data, s3_bucket[1])
        else:
            user_information = user_information_data(data, None)
        query = "SELECT * FROM users.user_view WHERE email = %s;"
        cursor.execute(query, (user_information['email'],))
        check_mail = cursor.fetchone()
        if check_mail:
            return jsonify({
                'success': False,
                'message': f"Email '{user_information['email']}' already exist.",
            }), status_code['HTTP_INTERNAL_SERVER_ERROR']
        query = "SELECT * FROM users.user_view WHERE phone_number = %s;"
        cursor.execute(query, (user_information['phone_number'],))
        check_phone_number = cursor.fetchone()
        if check_phone_number:
            return jsonify({
                'success': False,
                'message': f"phone_number '{user_information['phone_number']}' already exist.",
            }), status_code['HTTP_INTERNAL_SERVER_ERROR']
        password_hash = hash_password(
            user_information['password_hash']).decode('utf-8')
        user_body = (user_information['username'], user_information['email'], password_hash, user_information['phone_number'], user_information['photo'], user_information['date_of_birth'],
                    user_information['religion'], user_information['community'], user_information['country'], user_information['gender'], user_information['education'], user_information['occupation'], user_information['about_me'], user_information['last_login_at'])
        cursor.execute(
            "SELECT * from users.insert_user(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", user_body)
        cursor.execute('SELECT id from users.user')
        data = cursor.fetchall()
        user_id = data[-1][0]
        connection.commit()
        return jsonify({
            "success": True,
            "message": "Registration successful",
        }), status_code['HTTP_OK']
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': status_message['HTTP_INTERNAL_SERVER_ERROR'],
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        cursor.close()
        conn.putconn(connection)


def user_preference(req):
    try:
        connection = conn.getconn()
        connection.autocommit = True
        cursor = connection.cursor()
        data = req
        user_preference_information = user_preference_data(data)
        cursor.execute('SELECT id from users.user')
        dataForUser = cursor.fetchall()
        max_value = max(dataForUser, key=lambda tup: tup[0])[0]
        max_tuple = max(dataForUser, key=lambda tup: tup[0])
        query = "SELECT * FROM users.user_preference WHERE user_id = %s;"
        cursor.execute(query, max_tuple,)
        check_user = cursor.fetchone()
        if check_user:
            return jsonify({
                'success': False,
                'message': f"user '{max_tuple}' already exist.",
            }), status_code['HTTP_INTERNAL_SERVER_ERROR']
        user_preference = (max_value, int(user_preference_information['from_age']), int(user_preference_information['to_age']), user_preference_information['desired_religion'], user_preference_information['desired_country'],
                        user_preference_information['desired_community'], user_preference_information['desired_occupation'], user_preference_information['desired_education'], user_preference_information['desired_language'], user_preference_information['desired_gender'], user_preference_information['desired_marital_status'])
        cursor.execute(
            "SELECT * from users.insert_user_preference(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                user_preference
            ))
        cursor.execute(
            'SELECT id, email, username, phone_number  from users.user WHERE id = %s', (max_value,))
        user_data = cursor.fetchall()
        # user_id = user_data[-1][0]
        # username = user_data[-1][2]
        email = user_data[-1][1]
        # phone_number = user_data[-1][3]
        connection.commit()
        # token_data = {
        #     "user_id": user_id,
        #     "username": username,
        #     "email": email,
        #     "phone_number": phone_number,
        # }
        # token = create_token(token_data, USER_SECRET)
        return jsonify({
            "success": True,
            "message": "Registration successful",
            "token": email
        }), status_code['HTTP_OK']
    except Exception as e:
        print(e)
        # Execute the DELETE statement
        cursor.execute("DELETE FROM users.user WHERE id = %s", (max_value,))
        connection.rollback()
        return jsonify({
            'success': False,
            'message': status_message['HTTP_INTERNAL_SERVER_ERROR'],
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        cursor.close()
        conn.putconn(connection)

def login_form():
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        data = request.json
        email = data.get("email")
        password = data.get("password")
        query = "SELECT * FROM users.user_view WHERE email = %s;"
        cursor.execute(query, (email,))
        check_mail = cursor.fetchone()
        query = "SELECT id FROM users.user_view WHERE email = %s;"
        cursor.execute(query, (email,))
        user_id = cursor.fetchone()
        query = "SELECT username FROM users.user_view WHERE email = %s;"
        cursor.execute(query, (email,))
        username = cursor.fetchone()
        query = "SELECT phone_number FROM users.user_view WHERE email = %s;"
        cursor.execute(query, (email,))
        phone_number = cursor.fetchone()
        if not check_mail:
            return jsonify({
                'success': False,
                'message': f"Email '{email}' doesn't exist.",
            }), status_code['HTTP_UNAUTHORIZED']
        queryForPass = "SELECT password_hash FROM users.user WHERE email = %s;"
        cursor.execute(queryForPass, (email,))
        hashed_password = cursor.fetchone()
        hash_password_extract = hashed_password[0]
        hash_password_str = str(hash_password_extract)
        checkVerify = verify_password(
            password.encode('utf-8'), hash_password_str.encode('utf-8'))
        if (not checkVerify):
            return jsonify({
                "success": False,
                "message": "Login failed",
            }), status_code['HTTP_UNAUTHORIZED']
        connection.commit()
        token_data = {
            "user_id": user_id[0],
            "username": username[0],
            "email": email,
            "phone_number": phone_number[0],
        }
        print("token", token_data)
        token = create_token(token_data, USER_SECRET)
        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token
        }), status_code['HTTP_OK']
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': status_message['HTTP_INTERNAL_SERVER_ERROR'],
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        cursor.close()
        conn.putconn(connection)
