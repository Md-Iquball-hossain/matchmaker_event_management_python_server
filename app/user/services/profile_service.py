# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint, jsonify, json, make_response, request
from app.database import conn
import traceback
from utils.s3_bucket.s3_bucket import Uploader
from psycopg2 import sql
import os
import uuid
from utils.miscellaneous.status_code import status_code
from utils.miscellaneous.response_message import status_message
from utils.logging.logging import app
from utils.services.service import create_exception_service
from werkzeug.datastructures import MultiDict
from utils.lib.file_manager import delete_files
profile = Blueprint("get_profile", __name__)

def get_profile(current_user):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        user = current_user['user_id']
        query = "SELECT * FROM users.user WHERE id = %s"
        cursor.execute(query, (user,))
        profile = cursor.fetchone()
        data_of_birth_data = {
            "date_of_birth": profile[6],
        }
        date_of_birth = data_of_birth_data['date_of_birth']
        profile_data = {
            "id": profile[0],
            "username": profile[1],
            "email": profile[2],
            "phone_number": profile[4],
            "photo": profile[5],
            "date_of_birth": date_of_birth.strftime('%Y-%m-%d'),
            "religion": profile[7],
            "community": profile[8],
            "country": profile[9],
            "gender": profile[10],
            "education": profile[11],
            "occupation": profile[12],
            "about_me": profile[13],
            "language": profile[16]
        }
        connection.commit()
        query = "SELECT * FROM users.user_preference WHERE user_id = %s"
        cursor.execute(query, (user,))
        user_preference = cursor.fetchone()
        if (not user_preference):
            return jsonify({
                'success': False,
                'message': status_message['HTTP_NOT_FOUND'],
            }), status_code['HTTP_NOT_FOUND']
        user_preference_data = {
            "from_age": user_preference[2],
            "to_age": user_preference[3],
            "desired_religion": user_preference[4].strip('{}'),
            # "desired_country": user_preference[5].strip('{}'),
            "desired_community": user_preference[6].strip('{}'),
            # "desired_occupation": user_preference[7].strip('{}'),
            # "desired_education": user_preference[8].strip('{}'),
            "desired_language": user_preference[9].strip('{}'),
            "desired_gender": user_preference[10].strip('{}'),
            # "desired_marital_status": user_preference[12].strip('{}')
        }
        desired_occupation = user_preference[7].strip('{}')
        user_preference_data["desired_occupation"] = desired_occupation.replace(
            '"', '')
        desired_marital_status = user_preference[11].strip('{}')
        user_preference_data["desired_marital_status"] = desired_marital_status.replace(
            '"', '')
        desired_education = user_preference[8].strip('{}')
        user_preference_data["desired_education"] = desired_education.replace(
            '"', '')
        desired_country = user_preference[5].strip('{}')
        user_preference_data["desired_country"] = desired_country.replace(
            '"', '')
        connection.commit()
        cursor.close()
        app.logger.info('Profile show successfully')
        return jsonify({
            "success": True,
            "message": "Profile show's successfully",
            "data": [profile_data, user_preference_data]
        }), status_code['HTTP_OK']
    except Exception as e:
        print(e)
        cursor.close()
        # app.logger.error(f'An exception occured: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': status_message['HTTP_INTERNAL_SERVER_ERROR'],
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        conn.putconn(connection)


def update_profile(current_user):
    connection = conn.getconn()
    cursor = connection.cursor()
    try:
        user_body = {}
        id = current_user['user_id']
        data = MultiDict(request.form)
        # file = request.files['photo']
        user_body = data
        file = request.files['photo'] if 'photo' in request.files else None
        if file:
            s3_bucket = Uploader.cloudUpload(file, "photo")
            user_body['photo'] = s3_bucket[1]
        set_clause = ', '.join(
            [f'{key} = %s' for key in user_body.keys()])
        update_values = {key: value for key, value in user_body.items()}
        update_values['id'] = id
        update_query = f"""
            UPDATE users.user
            SET {set_clause}
            WHERE id = %s
            """
        cursor.execute(update_query, tuple(update_values.values()))
        connection.commit()
        app.logger.info('Profile show successfully')
        return jsonify({
            "success": True,
            "message": "Profile Updated successfully",
        }), status_code['HTTP_OK']
    except Exception as e:
        print(e)
        app.logger.error(f'An exception occured: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': status_message['HTTP_INTERNAL_SERVER_ERROR'],
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        cursor.close()
        conn.putconn(connection)
