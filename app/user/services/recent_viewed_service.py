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
recent_view = Blueprint("my_matches_list", __name__)


def recent_view_data(current_user):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        connection.autocommit = False

        viewer = current_user['user_id']
        viewed = request.args.get('id')

        cursor.callproc(
            'users.save_profile_view',
            (
                viewer, viewed
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


def get_recent_view_data(current_user):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        viewer = current_user['user_id']


        query = "SELECT * FROM users.profile_views WHERE viewer_id = %s;"
        cursor.execute(query, (viewer,))

        rows = cursor.fetchall()


        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        store = []

        for entry in results:
            store.append(entry['viewed_profile_id'])

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


def get_visitor(current_user):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        viewer = current_user['user_id']


        query = "SELECT * FROM users.profile_views WHERE viewed_profile_id = %s;"
        cursor.execute(query, (viewer,))

        rows = cursor.fetchall()


        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        store = []

        for entry in results:
            store.append(entry['viewer_id'])

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