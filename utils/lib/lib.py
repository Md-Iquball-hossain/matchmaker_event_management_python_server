# Author: Shidul Islam
# Date: 10-11-2023
# */

import bcrypt
import jwt
import random
from flask_mail import Mail, Message
from flask import current_app
from config import EMAIL_ID
from utils.miscellaneous.constants import numbers


def hash_password(password):
    salt = bcrypt.gensalt(10)
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, salt)


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password, hashed_password)


def create_token(payload, secret):
    return jwt.encode(payload, secret, algorithm="HS256")


def verify_token(token, secret):
    try:
        decoded_payload = jwt.decode(token, secret, algorithms=["HS256"])
        print("JWt is valid. Decoded payload:", decoded_payload)
    except jwt.ExpiredSignatureError:
        print("JWT has expired")
    except jwt.DecodeError:
        print("JWT decoding error. Token is invalid")


def otp_generate(length):
    otp = ''
    for number in range(length):
        ran = random.randint(0, (len(numbers) - 1))
        a = str(ran)
        otp += a

    return otp


def send_mail(recipient_email, subject, body):
    try:
        mail = Mail(current_app)
        message = Message(subject=subject, sender=EMAIL_ID,
                recipients=[recipient_email])
        message.body = body
        mail.send(message)
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
