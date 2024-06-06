
#---------------------------------- Topics : vendor authentication all API service, Author: Md. Iquball Hossain, Date: 21-11-2023 ---------------------

import boto3, uuid, os, bcrypt
from flask import Blueprint, jsonify, request
import jwt
from app.database import conn
from utils.s3_bucket.s3_bucket import Uploader
from utils.lib.lib import create_token,hash_password,verify_password
from utils.miscellaneous.status_code import status_code
from config import AWS_S3_BUCKET, AWS_S3_ACCESS_KEY, AWS_S3_SECRET_KEY, VENDOR_SECRET
from utils.miscellaneous.response_message import status_message

auth_vendor_service = Blueprint("auth_vendor_service", __name__)

#---------------------------------- Topics : vendor registration (sign-up) API service, Author: Md. Iquball Hossain, Date: 21-11-2023 ---------------------

def signup_vendor():
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        data = request.form.to_dict()
        file_photo = request.files.get('photo')
        file_tin_certificate = request.files.get('tin_certificate')
        required_fields = ['org_name', 'org_username', 'email', 'password', 'phone_number', 'address']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f"Missing or empty field: {field}",
                }), status_code['HTTP_BAD_REQUEST']
        email = data['email']
        cursor.execute("SELECT * FROM vendors.vendor WHERE email = %s;", (email,))
        check_email = cursor.fetchone()
        if check_email:
            return jsonify({
                'success': False,
                'message': f"Email '{email}' already exists for a vendor.",
            }), status_code['HTTP_INTERNAL_SERVER_ERROR']
        org_name = data['org_name']
        org_username = data['org_username']
        cursor.execute("SELECT * FROM vendors.vendor WHERE org_username = %s;", (org_username,))
        check_username = cursor.fetchone()
        if check_username:
            return jsonify({
                'success': False,
                'message': f"Username '{org_username}' already exists for a vendor.",
            }), status_code['HTTP_INTERNAL_SERVER_ERROR']
        phone_number = data['phone_number']
        cursor.execute("SELECT * FROM vendors.vendor WHERE phone_number = %s;", (phone_number,))
        check_phone = cursor.fetchone()
        if check_phone:
            return jsonify({
                'success': False,
                'message': f"Phone number '{phone_number}' already exists for a vendor.",
            }), status_code['HTTP_INTERNAL_SERVER_ERROR']
        password = data['password']
        hashed_password = hash_password(password)
        address = data['address']
        city = data.get('city', 'Dhaka') 
        country = data.get('country', 'Bangladesh') 
        business_category = data.get('business_category', 'Photography')
        details = data.get('details')
        last_login_at = data.get('last_login_at')
        photo = None
        if file_photo:
            success_photo, key_photo = Uploader.cloudUpload(file_photo, "vendor_photos")
            if success_photo:
                photo = key_photo
        tin_certificate = None
        if file_tin_certificate:
            success_tin_cert, key_tin_cert = Uploader.cloudUpload(file_tin_certificate, "tin_certificates")
            if success_tin_cert:
                tin_certificate = key_tin_cert
        cursor.execute(
            "INSERT INTO vendors.vendor (org_name, org_username, email, password_hash, phone_number, address, city, country, business_category, details, last_login_at, photo, tin_certificate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (org_name, org_username, email, hashed_password, phone_number, address, city, country, business_category, details, last_login_at, photo, tin_certificate)
        )
        connection.commit()
        response = {
            "message": "Vendor registration successful",
            "org_name": org_name,
            "org_username": org_username,
            "email": email,
            "phone_number": phone_number,
            "address": address,
            "city": city,
            "country": country,
            "details": details,
            "business_category": business_category,
            "tin_certificate": tin_certificate,
        }
        token_data = {
            "id": cursor.lastrowid,
            "org_username": org_username,
            "email": email,
            "phone_number": phone_number,
        }
        token = create_token(token_data, VENDOR_SECRET)
        response_with_token = {
            **response,
            'token': token,
            'success': True
        }
        return jsonify(response_with_token), status_code['HTTP_OK']
    except KeyError as key_error:
        return jsonify({
            'success': False,
            'message': f"Missing key in request data: {str(key_error)}",
        }), status_code['HTTP_BAD_REQUEST']
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': f'An error occurred while processing the request: {str(e)}',
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        cursor.close()
        conn.putconn(connection)

#---------------------------------- Topics : vendor login Hash password and verify password function, Author: Md. Iquball Hossain, Date: 22-11-2023 ---------------------

def hash_password(password):
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Error verifying password: {str(e)}")
        return False

#---------------------------------- Topics : vendor registration Photo upload function, Author: Md. Iquball Hossain, Date: 22-11-2023 ---------------------

class Uploader:
    def cloudUpload(file, folder):
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_S3_ACCESS_KEY,
            aws_secret_access_key=AWS_S3_SECRET_KEY,
            region_name='ap-south-1'
        )
        try:
            ext = os.path.splitext(file.filename)[-1]
            random_filename = str(uuid.uuid4()) + ext
            key = f"match360/{folder}/{random_filename}"
            s3.upload_fileobj(file, AWS_S3_BUCKET, key)
            return True, key
        except Exception as e:
            s3.delete_object(Bucket=AWS_S3_BUCKET, Key="photo")
            return False, str

#---------------------------------- Topics : create token and verify token function for login, Author: Md. Iquball Hossain, Date: 22-11-2023 ---------------------

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

#---------------------------------- Topics : vendor login (sign-in) API service, Author: Md. Iquball Hossain, Date: 22-11-2023 ---------------------

def login_vendor():
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        data = request.json
        email_or_username = data.get("email_or_username")
        password = data.get("password")
        query = "SELECT id, org_username, email, phone_number, password_hash, vendor_profile_status FROM vendors.vendor WHERE email = %s OR org_username = %s;"
        cursor.execute(query, (email_or_username, email_or_username))
        vendor_data = cursor.fetchone()
        if not vendor_data:
            return jsonify({
                'success': False,
                'message': f"Vendor with provided credentials doesn't exist.",
            }), status_code['HTTP_UNAUTHORIZED']
        id, org_username, fetched_email, phone_number, hashed_password, profile_status = vendor_data
        if profile_status == 'blocked':
            return jsonify({
                'success': False,
                'message': 'Your vendor profile is blocked. Please contact support for assistance.',
            }), status_code['HTTP_FORBIDDEN']
        if not verify_password(password, hashed_password):
            return jsonify({
                "success": False,
                "message": "Incorrect password",
            }), status_code['HTTP_UNAUTHORIZED']
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        update_query = "UPDATE vendors.vendor SET last_login_at = %s, vendor_status = TRUE WHERE id = %s"
        cursor.execute(update_query, (current_time, id))
        connection.commit()
        token_data = {
            "id": id,
            "org_username": org_username,
            "email": fetched_email,
            "phone_number": phone_number,
        }
        token = create_token(token_data, VENDOR_SECRET)
        return jsonify({
            "success": True,
            "message": "Vendor login successful",
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
