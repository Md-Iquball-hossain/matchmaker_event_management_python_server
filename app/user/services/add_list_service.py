# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint, jsonify, request
from app.database import conn
import json
from psycopg2 import sql
from collections import namedtuple
from utils.miscellaneous.status_code import status_code
from utils.miscellaneous.response_message import status_message
from utils.logging.logging import app
from utils.services.service import create_exception_service
from app.user.utils.calculate_match_score import match_score
add_to_list = Blueprint("add_to_list", __name__)


def add_to_short_list(current_user):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        connection.autocommit = False

        user = current_user['user_id']
        favourite_id = request.args.get('id')
        req = request.get_json()
        is_like = req['favourite']

        check_multiple_fav = "SELECT favourite_id FROM users.favourite_list WHERE favourite_id = %s;"
        cursor.execute(check_multiple_fav, (favourite_id,))

        check_multiple = cursor.fetchall()

        if len(check_multiple) > 0:
            return jsonify({
                'success': False,
                "message": "can't stay multiple favourite's ID"
            }), status_code['HTTP_NOT_FOUND']

        cursor.callproc(
            'users.add_to_favourite_list',
            (
                user, favourite_id, is_like
            )
        )

        connection.commit()
        return jsonify({
            "success": True,
            "message": status_message['HTTP_OK'],
            "data": "Data inserted successfully",
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


def get_favourite_list(current_user):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        viewer = current_user['user_id']

        query = "SELECT * FROM users.favourite_list WHERE user_id = %s;"
        cursor.execute(query, (viewer,))

        # cursor.execute('SELECT * FROM users.favourite_list')

        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        store = []

        for entry in results:
            store.append(entry['favourite_id'])

        unique_viewed_profile_ids = set(store)

        data = []

        for viewed_profile_id in unique_viewed_profile_ids:
            query = "SELECT * FROM users.user WHERE id = %s"
            cursor.execute(query, (viewed_profile_id,))
            user = cursor.fetchone()
            data.append(user)

        column_names = ["id", "username", "email", "password_hash", "phone_number", "photo", "date_of_birth", "religion", "community",
                        "country", "gender", "education", "occupation", "about_me", "created_at", "last_login_at", "language", "age"]

        users = []

        for user_info in data:
            if user_info is not None:
                user_data_dict = dict(zip(column_names, user_info))
                users.append(user_data_dict)

        # Paginate the results
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = users[start_idx:end_idx]

        total = len(paginated_results)

        return jsonify({
            "success": True,
            "message": status_message['HTTP_OK'],
            "total": total,
            "data": paginated_results,
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


def add_dislike(current_user):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        connection.autocommit = False

        user = current_user['user_id']
        favourite_id = request.args.get('id')
        req = request.get_json()
        is_like = req['favourite']

        cursor.execute(
            "DELETE FROM users.favourite_list WHERE favourite_id = %s AND is_favourite = %s", (favourite_id, is_like))

        connection.commit()
        return jsonify({
            "success": True,
            "message": status_message['HTTP_OK'],
            "data": "Data removed from favourite list",
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
