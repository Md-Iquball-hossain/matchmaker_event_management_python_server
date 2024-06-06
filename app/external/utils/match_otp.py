from flask import Blueprint, jsonify, request
from app.database import conn
from utils.miscellaneous.response_message import status_message
from utils.miscellaneous.status_code import status_code
from utils.miscellaneous.constants import VERIFY_USER, EMAIL_OTP_TIME
from utils.lib.lib import hash_password, send_mail, verify_password
from utils.templates.sendEmailOtp import send_email_otp
from utils.miscellaneous.email_constant import EMAIL_OTP_SUBJECT
from config import USER_SECRET
from utils.lib.lib import hash_password, create_token, verify_password


# Verify user send otp service


def match_otp(email, type, otp):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        connection.autocommit = False

        query = "SELECT email, hashedotp FROM dbo.email_otp_view WHERE email = %s;"
        cursor.execute(query, (email,))

        otp_info = cursor.fetchone()

        query = "SELECT hashedotp FROM dbo.email_otp_view WHERE email = %s;"
        cursor.execute(query, (email,))
        last_otp = cursor.fetchall()

        if not otp_info[0]:
            return jsonify({
                'success': False,
                "message": status_message['HTTP_NOT_FOUND']
            }), status_code['HTTP_NOT_FOUND']

        encoded_string1 = str(otp)
        encode_hashed = str(last_otp[-1][0])
        match = verify_password(encoded_string1.encode(
            'utf-8'), encode_hashed.encode('utf-8'))

        if not match:
            return jsonify({
                "success": False,
                "message": status_message['HTTP_UNAUTHORIZED'],
            }), status_code['HTTP_UNAUTHORIZED']

        # Matched
        update_body = {
            "matched": 1
        }
        otp_body_update = ', '.join(
            [f'{key} = %s' for key in update_body.keys()])
        update_values = tuple(update_body.values())

        sql_query = f'UPDATE dbo.email_otp SET {otp_body_update} WHERE email = %s'

        cursor.execute(sql_query, update_values + (email,))

        # User Id fetch
        query = "SELECT id, username, phone_number FROM users.user_view WHERE email = %s;"
        cursor.execute(query, (email,))

        user = cursor.fetchone()

        token_data = {
            "user_id": user[0],
            "username": user[1],
            "email": otp_info[0],
            "phone_number": user[2],
        }

        token = create_token(token_data, USER_SECRET)

        connection.commit()

        return jsonify({
            'success': True,
            "message": status_message['HTTP_SUCCESSFUL'],
            "token": token
        }), status_code['HTTP_SUCCESSFUL']

    except Exception as e:
        print(e)
        raise Exception(e)
    finally:
        cursor.close()
        conn.putconn(connection)
