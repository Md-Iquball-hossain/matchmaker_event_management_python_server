import boto3, uuid, os, bcrypt
from flask import Blueprint, jsonify, request
from datetime import datetime
import jwt
import app
from app.database import conn
from utils.s3_bucket.s3_bucket import Uploader
from utils.miscellaneous.status_code import status_code
from config import ADMIN_SECRET, AWS_S3_ACCESS_KEY, AWS_S3_BUCKET, AWS_S3_SECRET_KEY
from utils.miscellaneous.response_message import status_message

admin_profile_service = Blueprint("admin_profile_service", __name__)

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

#---------------------------------- Topics : Admin profile, Author: Md. Iquball Hossain, Date: 06-12-2023 ---------------------

def create_admin_profile(current_admin):
    try:
        if current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can create a new admin profile.',
            }), status_code['HTTP_FORBIDDEN']
        connection = conn.getconn()
        cursor = connection.cursor()
        data = request.form.to_dict()
        file_admin_photo = request.files.get('admin_photo')
        required_fields = ['admin_role', 'admin_username', 'admin_email', 'admin_password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f"Missing or empty field: {field}",
                }), status_code['HTTP_BAD_REQUEST']
        admin_email = data['admin_email']
        cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_email = %s;", (admin_email,))
        check_admin_email = cursor.fetchone()
        if check_admin_email:
            return jsonify({
                'success': False,
                'message': f"Email '{admin_email}' already exists for an Admin.",
            }), status_code['HTTP_INTERNAL_SERVER_ERROR']
        admin_username = data['admin_username']
        cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_username = %s;", (admin_username,))
        check_admin_username = cursor.fetchone()
        if check_admin_username:
            return jsonify({
                'success': False,
                'message': f"Username '{admin_username}' already exists for an Admin.",
            }), status_code['HTTP_INTERNAL_SERVER_ERROR']
        admin_phone = data.get('admin_phone')
        if admin_phone:
            cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_phone = %s;", (admin_phone,))
            check_admin_phone = cursor.fetchone()
            if check_admin_phone:
                return jsonify({
                    'success': False,
                    'message': f"Phone number '{admin_phone}' already exists for an Admin.",
                }), status_code['HTTP_INTERNAL_SERVER_ERROR']
        admin_password = data['admin_password']
        admin_password = hash_password(admin_password)
        admin_role = data['admin_role']
        admin_role_id = data['admin_role_id']
        admin_status = data.get('admin_status', True)
        admin_photo = None
        admin_role_category = data.get('admin_role_category', 'Default Category')
        if file_admin_photo:
            success_photo, key_photo = Uploader.cloudUpload(file_admin_photo, "admin_photos")
            if success_photo:
                admin_photo = key_photo
        cursor.execute(
            "INSERT INTO admin.admin_profile (admin_role, admin_username, admin_email, admin_password, admin_phone, admin_role_id, admin_photo, admin_status, admin_role_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (admin_role, admin_username, admin_email, admin_password, admin_phone, admin_role_id, admin_photo, admin_status, admin_role_category)
        )
        connection.commit()
        response = {
            "message": "Admin registration successful",
            "admin_role": admin_role,
            "admin_username": admin_username,
            "admin_email": admin_email,
            "admin_phone": admin_phone,
            "admin_role_id": admin_role_id,
            "admin_photo": admin_photo,
            "admin_role_category": admin_role_category
        }
        return jsonify(response), status_code['HTTP_OK']
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

#---------------------------------- Topics : Admin login (sign-in) API service, Author: Md. Iquball Hossain, Date: 06-12-2023 ---------------------

def login_admin():
    cursor = None
    connection = None
    try:
        data = request.form.to_dict()
        email_or_username = data.get("email_or_username")
        password = data.get("password")
        connection = conn.getconn()
        cursor = connection.cursor()
        query = "SELECT admin_id, admin_username, admin_email, admin_phone, admin_password, admin_role, admin_status FROM admin.admin_profile WHERE admin_email = %s OR admin_username = %s;"
        cursor.execute(query, (email_or_username, email_or_username))
        admin_data = cursor.fetchone()
        if not admin_data:
            return jsonify({
                'success': False,
                'message': f"Admin with provided credentials doesn't exist.",
            }), status_code['HTTP_UNAUTHORIZED']
        admin_id, admin_username, fetched_admin_email, admin_phone, hashed_password, admin_role, admin_status = admin_data
        if not admin_status: 
            return jsonify({
                'success': False,
                'message': 'Your profile is deactivated. Please contact the administrator.',
            }), status_code['HTTP_FORBIDDEN']
        if not verify_password(password, hashed_password):
            return jsonify({
                "success": False,
                "message": "Incorrect password",
            }), status_code['HTTP_UNAUTHORIZED']
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_query = "UPDATE admin.admin_profile SET admin_last_login_time = %s WHERE admin_id = %s"
        cursor.execute(update_query, (current_time, admin_id))
        connection.commit()
        token_data = {
            "admin_id": admin_id,
            "admin_username": admin_username,
            "admin_email": fetched_admin_email,
            "admin_phone": admin_phone,
            "admin_role": admin_role
        }
        token = create_token(token_data, ADMIN_SECRET)
        return jsonify({
            "success": True,
            "message": "Admin login successful",
            "token": token
        }), status_code['HTTP_OK']
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': status_message['HTTP_INTERNAL_SERVER_ERROR'],
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        if cursor:
            cursor.close()
        if connection:
            conn.putconn(connection)

#---------------------------------- Topics : Admin profile multiple view service, Author: Md. Iquball Hossain, Date: 07-12-2023 ---------------------

def view_admin_profile_list(current_admin):
    cursor = None
    connection = None
    try:
        if not current_admin or not current_admin.get('admin_id'):
            return jsonify({
                'success': False,
                'message': 'Unauthorized access: Invalid admin ID'
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        if current_admin['admin_role'].lower() == 'super admin':
            cursor.execute("SELECT * FROM admin.admin_profile ORDER BY admin_id DESC")
        else:
            cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_id = %s ORDER BY admin_id DESC", (current_admin['admin_id'],))
        admin_profiles = cursor.fetchall()
        formatted_profiles = []
        for admin_profile in admin_profiles:
            admin_create_time = admin_profile[8]
            admin_last_login_time = admin_profile[9]
            admin_create_date = admin_create_time.strftime("%Y-%m-%d") if admin_create_time else None
            admin_create_time_formatted = admin_create_time.strftime("%I:%M %p") if admin_create_time else None
            admin_last_login_date = admin_last_login_time.strftime("%Y-%m-%d") if admin_last_login_time else None
            admin_last_login_time_formatted = admin_last_login_time.strftime("%I:%M %p") if admin_last_login_time else None
            formatted_profile = {
                'admin_id': admin_profile[0],
                'admin_username': admin_profile[1],
                'admin_email': admin_profile[2],
                'admin_phone': admin_profile[4],
                'admin_password': admin_profile[3],
                'admin_role': admin_profile[5],
                'admin_role_id': admin_profile[6],
                'admin_photo': admin_profile[7],
                'admin_create_date': admin_create_date,
                'admin_create_time': admin_create_time_formatted,
                'admin_last_login_date': admin_last_login_date,
                'admin_last_login_time': admin_last_login_time_formatted,
                'admin_status': admin_profile[10],
                'admin_role_category': admin_profile[11]
            }
            formatted_profiles.append(formatted_profile)
        return jsonify({
            'success': True,
            'message': 'Admin profiles retrieved successfully',
            'data': formatted_profiles
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred while fetching the admin profiles: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            conn.putconn(connection)

#---------------------------------- Topics : Single admin profile view service, Author: Md. Iquball Hossain, Date: 07-12-2023 ---------------------

def get_single_admin_profiles(current_admin):
    cursor = None
    connection = None
    try:
        if not current_admin or not current_admin.get('admin_id'):
            return jsonify({
                'success': False,
                'message': 'Unauthorized access: Invalid admin ID'
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_id = %s ORDER BY admin_id DESC", (current_admin['admin_id'],))
        admin_profiles = cursor.fetchall()
        formatted_profiles = []
        for admin_profile in admin_profiles:
            admin_create_time = admin_profile[8]
            admin_last_login_time = admin_profile[9]
            admin_create_date = admin_create_time.strftime("%Y-%m-%d") if admin_create_time else None
            admin_create_time_formatted = admin_create_time.strftime("%I:%M %p") if admin_create_time else None
            admin_last_login_date = admin_last_login_time.strftime("%Y-%m-%d") if admin_last_login_time else None
            admin_last_login_time_formatted = admin_last_login_time.strftime("%I:%M %p") if admin_last_login_time else None
            formatted_profile = {
                'admin_id': admin_profile[0],
                'admin_username': admin_profile[1],
                'admin_email': admin_profile[2],
                'admin_phone': admin_profile[4],
                'admin_password': admin_profile[3],
                'admin_role': admin_profile[5],
                'admin_role_id': admin_profile[6],
                'admin_photo': admin_profile[7],
                'admin_create_date': admin_create_date,
                'admin_create_time': admin_create_time_formatted,
                'admin_last_login_date': admin_last_login_date,
                'admin_last_login_time': admin_last_login_time_formatted,
                'admin_status': admin_profile[10],
                'admin_role_category': admin_profile[11]
            }
            formatted_profiles.append(formatted_profile)
        return jsonify({
            'success': True,
            'message': 'Admin profiles retrieved successfully',
            'data': formatted_profiles
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred while fetching the admin profiles: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            conn.putconn(connection)

#---------------------------------- Topics : Super Admin view specific admin profile, Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

def superadmin_get_specific_admin_profile(current_admin,admin_id):
    cursor = None
    connection = None
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view user profiles.',
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_id = %s", (admin_id,))
        admin_profile = cursor.fetchone()
        if admin_profile:
            admin_create_time = admin_profile[8]
            admin_last_login_time = admin_profile[9]
            admin_create_date = admin_create_time.strftime("%Y-%m-%d") if admin_create_time else None
            admin_create_time_formatted = admin_create_time.strftime("%I:%M %p") if admin_create_time else None
            admin_last_login_date = admin_last_login_time.strftime("%Y-%m-%d") if admin_last_login_time else None
            admin_last_login_time_formatted = admin_last_login_time.strftime("%I:%M %p") if admin_last_login_time else None
            formatted_profile = {
                'admin_id': admin_profile[0],
                'admin_username': admin_profile[1],
                'admin_email': admin_profile[2],
                'admin_phone': admin_profile[4],
                'admin_password': admin_profile[3],
                'admin_role': admin_profile[5],
                'admin_role_id': admin_profile[6],
                'admin_photo': admin_profile[7],
                'admin_create_date': admin_create_date,
                'admin_create_time': admin_create_time_formatted,
                'admin_last_login_date': admin_last_login_date,
                'admin_last_login_time': admin_last_login_time_formatted,
                'admin_status': admin_profile[10],
                'admin_role_category': admin_profile[11]
            }
            return jsonify({
                'success': True,
                'message': f'Admin profile with id {admin_id} retrieved successfully',
                'data': formatted_profile
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'No admin profile found for id {admin_id}'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred while fetching the admin profile: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            conn.putconn(connection)

#---------------------------------- Topics : Super Admin edit specific Admin profile service , Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

def update_specific_admin(current_admin,admin_id):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view user profiles.',
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        data = request.form.to_dict()
        file_admin_photo = request.files.get('admin_photo')
        email = request.form.get('admin_email')
        if email:
            cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_email = %s AND admin_id != %s;", (email, admin_id))
            existing_admin = cursor.fetchone()
            if existing_admin:
                return jsonify({
                    'success': False,
                    'message': 'Email already exists in another admin profile.',
                }), status_code['HTTP_BAD_REQUEST']
        cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_id = %s;", (admin_id,))
        admin_profile = cursor.fetchone()
        if not admin_profile:
            return jsonify({
                'success': False,
                'message': f"No admin profile found for ID {admin_id}",
            }), status_code['HTTP_NOT_FOUND']
        admin_role = data.get('admin_role', admin_profile[5])
        admin_role_id = data.get('admin_role_id', admin_profile[6])
        admin_role_category = data.get('admin_role_category', admin_profile[7])
        admin_status = data.get('admin_status', admin_profile[10])
        admin_email = email if email else admin_profile[4]
        update_query = """
            UPDATE admin.admin_profile 
            SET 
                admin_role = %s, 
                admin_role_id = %s, 
                admin_role_category = %s, 
                admin_status = %s,
                admin_email = %s
        """
        update_values = [admin_role, admin_role_id, admin_role_category, admin_status, admin_email]
        if file_admin_photo:
            success_photo, key_photo = Uploader.cloudUpload(file_admin_photo, "admin_photos")
            if success_photo:
                update_query += ", admin_photo = %s"
                update_values.append(key_photo)
        update_query += " WHERE admin_id = %s;"
        update_values.append(admin_id)
        cursor.execute(update_query, tuple(update_values))
        connection.commit()
        return jsonify({
            'success': True,
            'message': f"Admin profile with ID {admin_id} updated successfully",
            'data': {
                'admin_id': admin_id,
                'admin_role': admin_role,
                'admin_role_id': admin_role_id,
                'admin_role_category': admin_role_category,
                'admin_status': admin_status,
                'admin_email': admin_email
            }
        }), status_code['HTTP_OK']
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred while updating the admin profile: {str(e)}',
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        cursor.close()
        conn.putconn(connection)

#---------------------------------- Topics : Admin personal profile edit service, Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

def update_admin_personal_profile(current_admin):
    try:
        if not current_admin or not current_admin.get('admin_id'):
            return jsonify({
                'success': False,
                'message': 'Unauthorized access: Invalid admin ID'
            }), status_code['HTTP_FORBIDDEN']
        connection = conn.getconn()
        cursor = connection.cursor()
        data = request.form.to_dict()
        file_admin_photo = request.files.get('admin_photo')
        admin_id = current_admin['admin_id']
        update_fields = {}
        if 'admin_username' in data:
            new_username = data['admin_username']
            cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_username = %s AND admin_id != %s;", (new_username, admin_id))
            existing_username = cursor.fetchone()
            if existing_username:
                return jsonify({
                    'success': False,
                    'message': 'Username already exists in another admin profile.',
                }), status_code['HTTP_BAD_REQUEST']
            update_fields['admin_username'] = new_username
        if 'admin_password' in data:
            update_fields['admin_password'] = hash_password(data['admin_password'])
        if 'admin_phone' in data:
            update_fields['admin_phone'] = data['admin_phone']
        if file_admin_photo:
            success_photo, key_photo = Uploader.cloudUpload(file_admin_photo, "admin_photos")
            if success_photo:
                update_fields['admin_photo'] = key_photo
        if update_fields:
            set_query = ', '.join([f"{key} = %s" for key in update_fields])
            update_values = [value for value in update_fields.values()]
            update_query = f"UPDATE admin.admin_profile SET {set_query} WHERE admin_id = %s RETURNING *;"
            update_values.append(admin_id)
            cursor.execute(update_query, tuple(update_values))
            updated_profile = cursor.fetchone()
            connection.commit()
            formatted_profile = {
                'admin_id': updated_profile[0],
                'admin_username': updated_profile[1],
                'admin_email': updated_profile[2],
                'admin_password': updated_profile[3],
                'admin_phone': updated_profile[4],
                'admin_role': updated_profile[5],
                'admin_role_id': updated_profile[6],
                'admin_photo': updated_profile[7],
                'admin_status': updated_profile[10]
            }
            return jsonify({
                'success': True,
                'message': f"Admin profile with ID {admin_id} updated successfully",
                'data': formatted_profile
            }), status_code['HTTP_OK']
        else:
            return jsonify({
                'success': False,
                'message': 'No fields provided for update'
            }), status_code['HTTP_BAD_REQUEST']
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred while updating the admin profile: {str(e)}',
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        cursor.close()
        conn.putconn(connection)

#---------------------------------- Topics : Delete Specific service, Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

def delete_admin_profile(current_admin,admin_id):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view user profiles.',
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM admin.admin_profile WHERE admin_id = %s;", (admin_id,))
        connection.commit()
        return jsonify({
            'success': True,
            'message': f"Admin profile with ID {admin_id} deleted successfully",
        }), status_code['HTTP_OK']
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred while deleting the admin profile: {str(e)}',
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        cursor.close()
        conn.putconn(connection)

#---------------------------------- Topics : Delete Specific service, Author: Md. Iquball Hossain, Date: 11-12-2023 ---------------------

def view_admin_profiles_by_status(current_admin, status):
    cursor = None
    connection = None
    try:
        if not current_admin or not current_admin.get('admin_id'):
            return jsonify({
                'success': False,
                'message': 'Unauthorized access: Invalid admin ID'
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        if status.lower() not in ['active', 'deactive']:
            return jsonify({
                'success': False,
                'message': 'Invalid status value. Use "active" or "deactive".'
            }), 400
        cursor.execute("SELECT * FROM admin.admin_profile WHERE admin_status = %s ORDER BY admin_id DESC;", (status.lower() == 'active',))
        admin_profiles = cursor.fetchall()
        formatted_profiles = []
        for admin_profile in admin_profiles:
            admin_create_time = admin_profile[8]
            admin_last_login_time = admin_profile[9]
            admin_create_date = admin_create_time.strftime("%Y-%m-%d") if admin_create_time else None
            admin_create_time_formatted = admin_create_time.strftime("%I:%M %p") if admin_create_time else None
            admin_last_login_date = admin_last_login_time.strftime("%Y-%m-%d") if admin_last_login_time else None
            admin_last_login_time_formatted = admin_last_login_time.strftime("%I:%M %p") if admin_last_login_time else None
            formatted_profile = {
                'admin_id': admin_profile[0],
                'admin_username': admin_profile[1],
                'admin_email': admin_profile[2],
                'admin_phone': admin_profile[4],
                'admin_role': admin_profile[5],
                'admin_role_id': admin_profile[6],
                'admin_photo': admin_profile[7],
                'admin_create_date': admin_create_date,
                'admin_create_time': admin_create_time_formatted,
                'admin_last_login_date': admin_last_login_date,
                'admin_last_login_time': admin_last_login_time_formatted,
                'admin_status': admin_profile[10],
                'admin_role_category': admin_profile[11]
            }
            formatted_profiles.append(formatted_profile)
        return jsonify({
            'success': True,
            'message': f'Admin profiles with status "{status}" retrieved successfully',
            'data': formatted_profiles
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred while fetching the admin profiles: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            conn.putconn(connection)