# Author: Shidul Islam
# Date: 10-11-2023
# */

from flask import Blueprint, jsonify, request
from app.database import conn
import json
import redis
# from utils.lib.redis_connect import redis_connects
from psycopg2 import sql
from collections import namedtuple
from utils.miscellaneous.status_code import status_code
from utils.miscellaneous.response_message import status_message
from utils.logging.logging import app
from utils.services.service import create_exception_service
from app.user.utils.calculate_match_score import match_score


def my_matches_list(current_user, filter_country=None, filter_religion=None, filter_occupation=None):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        # cache_data = redis_connect.get('my_match_list')
        # if cache_data:
        #     print("from cache")
        #     return cache_data

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        filter_religion = request.args.get('filter_religion')
        filter_religions = filter_religion.split(
            ',') if filter_religion else []

        filter_country = request.args.get('filter_country')
        filter_countries = filter_country.split(
            ',') if filter_country else []

        filter_occupation = request.args.get('filter_occupation')
        filter_occupations = filter_occupation.split(
            ',') if filter_occupation else []

        user = current_user['user_id']

        query = "SELECT * FROM users.user WHERE id = %s"
        cursor.execute(query, (user,))
        user_preference = cursor.fetchone()

        desired_religion = user_preference[7]
        desired_community = user_preference[8]
        desired_country = user_preference[9]
        desired_language = user_preference[16]
        user_preference_male_or_female = user_preference[10]

        cursor.callproc(
            'users.get_user_matching_profiles',
            (
                desired_religion, desired_community, desired_country, desired_language, user_preference_male_or_female, user
            )
        )

        # Fetch the results
        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        # Apply additional filters if provided
        if filter_country == 'all':
            pass
        else:
            results = [profile for profile in results if profile.get(
                'country') in filter_countries]

        if filter_religion == 'all':
            pass
        else:
            results = [profile for profile in results if profile.get(
                'religion') in filter_religions]

        if filter_occupation == 'all':
            pass
        else:
            results = [profile for profile in results if profile.get(
                'occupation') in filter_occupations]

        # Paginate the results
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = results[start_idx:end_idx]

        total = len(paginated_results)

        # cache_data = redis_connect.get('my_match_list', {"success": True,
        #                                                  "message": status_message['HTTP_OK'],
        #                                                  "total": total,
        #                                                  "data": paginated_results})

        connection.commit()
        print("from DB")
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


def my_matches_single_preference(current_user, id):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        cursor.execute(
            sql.SQL("SELECT * FROM users.get_user_with_preferences(%s)"), (id,))

        # Fetch the results
        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        connection.commit()

        return jsonify({
            "success": True,
            "message": status_message['HTTP_OK'],
            "data": results[0],
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


def my_matches_single_list_preference(current_user, id):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        cursor.execute(
            sql.SQL("SELECT * FROM users.get_user_with_preferences(%s)"), (id,))

        # Fetch the results
        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        connection.commit()

        return jsonify({
            "success": True,
            "message": status_message['HTTP_OK'],
            "data": results,
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


def todays_matches_list(current_user):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        user = current_user['user_id']

        query = "SELECT * FROM users.user WHERE id = %s"
        cursor.execute(query, (user,))
        user_preference = cursor.fetchone()

        desired_country = user_preference[9]
        desired_language = user_preference[16]
        user_preference_male_or_female = user_preference[10]

        cursor.callproc(
            'users.get_user_todays_match',
            (
                user, desired_country, desired_language, user_preference_male_or_female
            )
        )

        # Fetch the results
        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        # ids = [item['id'] for item in results]

        id_object = [{"id": item['id']} for item in results]

        total = len(results)

        return jsonify({
            "success": True,
            "message": status_message['HTTP_OK'],
            "total": total,
            "data": id_object,
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


def near_me_list(current_user, filter_country=None, filter_religion=None, filter_occupation=None, filter_email=None):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        filter_religion = request.args.get('filter_religion')
        filter_religions = filter_religion.split(
            ',') if filter_religion else []

        filter_country = request.args.get('filter_country')
        filter_countries = filter_country.split(
            ',') if filter_country else []

        filter_occupation = request.args.get('filter_occupation')
        filter_occupations = filter_occupation.split(
            ',') if filter_occupation else []

        user_id = current_user['user_id']

        query = "SELECT * FROM users.user WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_preference = cursor.fetchone()

        desired_country = user_preference[9]
        user_preference_male_or_female = user_preference[10]

        cursor.callproc(
            'users.get_near_me_profiles_with_favourites',
            (
                desired_country, user_preference_male_or_female, user_id
            )
        )

        # Fetch the results
        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        # Apply additional filters if provided
        if filter_country == 'all':
            pass
        else:
            results = [profile for profile in results if profile.get(
                'country') in filter_countries]
        if filter_country == 'all':
            pass
        else:
            results = [profile for profile in results if profile.get(
                'religion') in filter_religions]
        if filter_country == 'all':
            pass
        else:
            results = [profile for profile in results if profile.get(
                'occupation') in filter_occupations]

        # Paginate the results
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = results[start_idx:end_idx]

        total = len(paginated_results)

        connection.commit()

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
