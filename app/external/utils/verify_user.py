from flask import Blueprint, jsonify, request
from app.database import conn
from utils.miscellaneous.response_message import status_message
from utils.miscellaneous.status_code import status_code
from utils.miscellaneous.constants import VERIFY_USER, EMAIL_OTP_TIME
from utils.lib.lib import hash_password, send_mail
from utils.templates.sendEmailOtp import send_email_otp
from utils.miscellaneous.email_constant import EMAIL_OTP_SUBJECT

# Verify user send otp service


def verify_user(email, otp):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        connection.autocommit = False
        query = "SELECT email FROM users.user_view WHERE email = %s;"
        cursor.execute(query, (email,))
        check_mail = cursor.fetchone()
        if not check_mail[0]:
            return jsonify({
                'success': False,
                "message": status_message['HTTP_NOT_FOUND']
            }), status_code['HTTP_NOT_FOUND']
        # check_otp = cursor.callproc(
        #     'dbo.call_email_otp', {"email": email, "type": VERIFY_USER, 'minute': EMAIL_OTP_TIME, 'matched': False})
        # user_body = (email, VERIFY_USER, EMAIL_OTP_TIME, False)
        # cursor.callproc('dbo.get_email_otp_by_criteria', user_body)
        # connection.commit()
        # check_otp = cursor.fetchone()
        # if check_otp:
        #     return jsonify({
        #         'success': False,
        #         "message": f"You cannot send OTP within {EMAIL_OTP_TIME} minutes"
        #     }), status_code['HTTP_FORBIDDEN']
        hashed_otp = hash_password(otp)
        hashed_otp_decode = hashed_otp.decode('utf-8')
        cursor.callproc('dbo.insert_email_data',
                        (hashed_otp_decode, email, VERIFY_USER))
        value = send_mail(email, EMAIL_OTP_SUBJECT,
                        send_email_otp(otp=otp, otp_for="verify user"))
        connection.commit()
        cursor.close()
        return jsonify({
            'success': True,
            "message": status_message['HTTP_SUCCESSFUL']
        }), status_code['HTTP_SUCCESSFUL']
    except Exception as e:
        print(e)
        connection.rollback()
        raise Exception(e)
    finally:
        cursor.close()
        conn.putconn(connection)
