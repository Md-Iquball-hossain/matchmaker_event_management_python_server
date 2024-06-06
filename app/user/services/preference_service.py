# Author: Shidul Islam
# Date: 10-11-2023
# */
from flask import Blueprint, jsonify, request
from app.database import conn
from utils.miscellaneous.status_code import status_code
from utils.miscellaneous.response_message import status_message
from utils.logging.logging import app
from utils.services.service import create_exception_service
preference = Blueprint("user_preference_data", __name__)


def user_preference_data(current_user):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        user = current_user['user_id']
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
            "desired_country": user_preference[5].strip('{}'),
            "desired_community": user_preference[6].strip('{}'),
            "desired_education": user_preference[8].strip('{}'),
            "desired_language": user_preference[9].strip('{}'),
            "desired_gender": user_preference[10].strip('{}')
        }
        desired_occupation = user_preference[7].strip('{}')
        user_preference_data["desired_occupation"] = desired_occupation.replace(
            '"', '')
        return jsonify({
            "success": True,
            "message": status_message['HTTP_OK'],
            "data": user_preference_data,
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


def user_preference_update(current_user):
    connection = conn.getconn()
    cursor = connection.cursor()
    try:
        preference_body = request.json
        user = current_user['user_id']
        update_query = "UPDATE users.user_preference SET"
        update_values = []
        for key, value in preference_body.items():
            if key == "desired_marital_status":
                update_query += f" {key} = %s::users.marital_status_type[],"
            elif key == "desired_language":
                update_query += f" {key} = %s::users.language_type[],"
            elif key == "desired_religion":
                update_query += f" {key} = %s::users.religion_type[],"
            elif key == "desired_country":
                update_query += f" {key} = %s::users.country_type[],"
            elif key == "desired_education":
                update_query += f" {key} = %s::users.education_type[],"
            elif key == "desired_gender":
                update_query += f" {key} = %s::users.gender_type[],"
            elif key == "desired_occupation":
                update_query += f" {key} = %s::users.occupation_type[],"
            elif key == "desired_community":
                update_query += f" {key} = %s::users.community_type[],"
            else:
                update_query += f" {key} = %s,"
            update_values.append(value)
        update_query = update_query[:-1] + " WHERE user_id = %s"
        update_values.append(user)
        cursor.execute(update_query, tuple(update_values))
        connection.commit()
        return jsonify({
            "success": True,
            "message": status_message['HTTP_OK'],
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