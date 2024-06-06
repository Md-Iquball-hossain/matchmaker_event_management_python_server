# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint, jsonify
from app.database import conn
import traceback
from utils.miscellaneous.status_code import status_code
from utils.miscellaneous.response_message import status_message
from utils.logging.logging import app
from utils.services.service import create_exception_service

#-----------------------  Topics : user profile list view (get) service, Modified: Md. Iquball Hossain, Date: 12-11-2023 -------------------------------------

admin_user_service = Blueprint("admin_user_service", __name__)

def get_user_list(current_admin):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view user profiles.',
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        query = "SELECT id, username, email, religion, country, gender FROM users.user"
        cursor.execute(query)
        user = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in user]
        connection.commit()
        cursor.close()
        conn.putconn(connection)
        app.logger.info('Profile show successfully')
        return jsonify({
            "success": True,
            "message": "User data show's successfully",
            "data": results
        }), status_code['HTTP_OK']
    except Exception as e:
        print(e)
        payload = {
            "exception_type": type(e).__name__,
            "exception_message": str(e),
            "stack_trace": traceback.format_exc(),
            "user_id": user
        }
        create_exception_service(payload)
        cursor.close()
        app.logger.error(f'An exception occured: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': status_message['HTTP_INTERNAL_SERVER_ERROR'],
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']

#-----------------------  Topics : user single profile view (get) service, Modified: Md. Iquball Hossain, Date: 12-11-2023 -------------------------------------

def get_user_single(current_admin,id):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view user profiles.',
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users.user WHERE id = %s ORDER BY created_at DESC", (id,))
        profiles = cursor.fetchall()
        cursor.close()
        conn.putconn(connection)
        if not profiles:
            return jsonify({
                'success': False,
                'message': f'No profiles found for User profile ID {id}',
            }), 404
        connection = conn.getconn()
        cursor = connection.cursor()
        user = id
        query = "SELECT * FROM users.user WHERE id = %s"
        cursor.execute(query, (user,))
        user = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description]
        results = dict(zip(column_names, user))
        connection.commit()
        cursor.close()
        conn.putconn(connection)
        app.logger.info('Single User show successfully')
        return jsonify({
            "success": True,
            "message": "Single User data show's successfully",
            "data": results
        }), status_code['HTTP_OK']
    except Exception as e:
        print(e)
        payload = {
            "exception_type": type(e).__name__,
            "exception_message": str(e),
            "stack_trace": traceback.format_exc(),
            "user_id": user
        }
        create_exception_service(payload)
        cursor.close()
        app.logger.error(f'An exception occured: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': status_message['HTTP_INTERNAL_SERVER_ERROR'],
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']

#-----------------------  Topics : user profile list view (get) according to gender, Modified: Md. Iquball Hossain, Date: 12-11-2023 -------------------------------------

ALLOWED_TYPES = ['Male', 'Female', 'Other']

def get_user_profiles_by_gender(current_admin, gender_type):
    try:
        if current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can create a new admin profile.',
            }), 403  
        if gender_type not in ALLOWED_TYPES:
            return jsonify({
                'success': False,
                'message': f'Invalid user gender type name. Allowed gender types are: {", ".join(ALLOWED_TYPES)}',
            }), 400
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users.user WHERE gender = %s ORDER BY created_at DESC", (gender_type,))
        profiles = cursor.fetchall()
        cursor.close()
        conn.putconn(connection)
        formatted_profiles = []
        for profile in profiles:
            formatted_profiles.append({
                'id': profile[0],
                'username': profile[1],
                'email': profile[2],
                'Password': profile[3],
                'phone_number': profile[4],
                'photo': profile[5],
                'date_of_birth': profile[6],
                'religion': profile[7], 
                'community': str(profile[8]),
                'country': profile[9],
                'gender': profile[10],
                'education': profile[11],
                'occupation': profile[12],
                'about_me': profile[13],
                'created_at':profile[14],
                'last_login_at':profile[15]  
            })
        return jsonify({
            'success': True,
            'message': f'All {gender_type} user profiles viewed successfully',
            'data': formatted_profiles
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500
