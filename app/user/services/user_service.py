from flask import request, jsonify
from flask import Blueprint, jsonify, request
from utils.s3_bucket.s3_bucket import Uploader
from app.database import conn
from datetime import datetime, time

user_service = Blueprint('user_service', __name__)

#----------------------------------  Topics : view user service list as business Category API Code, Author: Md. Iquball Hossain, Date: 24-12-2023 ----------------------

ALLOWED_CATEGORY = ['Photography', 'Catering', 'Music Band', 'Outdoor venue', 'Indoor Venue','Cake', 'Beauty and Makeup']

def user_get_vendors_by_business_category(current_user, business_category):
    try:
        if not current_user or 'user_id' not in current_user:
            return jsonify({'success': False, 'message': 'Invalid user token provided.'}), 401
        user_id = current_user['user_id']
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users.user WHERE id = %s", (user_id,))
        user_exists = cursor.fetchone()
        if not user_exists:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} does not exist in the system.',
            }), 401
        if business_category not in ALLOWED_CATEGORY:
            return jsonify({
                'success': False,
                'message': f'Invalid business category. Allowed categories are: {", ".join(ALLOWED_CATEGORY)}',
            }), 400
        cursor.execute("""
        SELECT v.*
        FROM vendors.vendor v
        INNER JOIN vendors.vendor_service vs ON v.id = vs.vendor_id
        WHERE v.business_category = 'Catering'
            AND v.vendor_profile_status = 'verified' 
            AND vs.vendor_service_status = true
        ORDER BY v.created_at DESC;
        """, (business_category,))
        profiles = cursor.fetchall()
        cursor.close()
        conn.putconn(connection)
        if not profiles:
            return jsonify({
                'success': False,
                'message': f'No profiles found for business category {business_category}',
            }), 404
        formatted_profiles = []
        for profile in profiles:
            formatted_profile = {
                'vendor_reg_id': profile[0],
                'org_name': profile[1],
                'org_username': profile[2],
                'email': profile[3],
                'phone_number': profile[5],
                'photo': profile[6],
                'address': profile[7],
                'city': profile[8],
                'country': profile[9],
                'details': profile[11],
                'vendor_profile_status': profile[15],
            }
            formatted_profiles.append(formatted_profile)
        return jsonify({
            'success': True,
            'message': f'Profiles for business category {business_category} viewed successfully',
            'data': formatted_profiles
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

#----------------------------------  Topics : view user single service using ID API Code, Author: Md. Iquball Hossain, Date: 24-12-2023 ---------------------

def user_get_vendors_by_id(current_user, vendor_id):
    try:
        if not current_user or 'user_id' not in current_user:
            return jsonify({'success': False, 'message': 'Invalid user token provided.'}), 401
        user_id = current_user['user_id']
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users.user WHERE id = %s", (user_id,))
        user_exists = cursor.fetchone()
        if not user_exists:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} does not exist in the system.',
            }), 401
        cursor.execute("SELECT * FROM vendors.vendor WHERE id = %s", (vendor_id,))
        vendor_profile = cursor.fetchone()
        cursor.execute("""
        SELECT vs.*
        FROM vendors.vendor_service vs
        WHERE vs.vendor_id = %s
        ORDER BY vs.vendor_service_id DESC
        LIMIT 1;
        """, (vendor_id,))
        vendor_service_data = cursor.fetchone()
        cursor.close()
        conn.putconn(connection)
        if vendor_profile and vendor_service_data:
            formatted_profile = {
                'vendor_reg_id': vendor_profile[0],
                'org_name': vendor_profile[1],
                'org_username': vendor_profile[2],
                'email': vendor_profile[3],
                'phone_number': vendor_profile[5],
                'photo': vendor_profile[6],
                'address': vendor_profile[7],
                'city': vendor_profile[8],
                'country': vendor_profile[9],
                'business_category': vendor_profile[10],
                'details': vendor_profile[11],
                'vendor_status': vendor_profile[14]
            }
            formatted_service = {
            'vendor_service_id': vendor_service_data[0],
            'vendor_id': vendor_service_data[1],
            'admin_id': vendor_service_data[2],
            'business_category_name': vendor_service_data[3],
            'business_type': vendor_service_data[4],
            'guest_capacity': vendor_service_data[5],
            'pricing_file': vendor_service_data[6],
            'social_media_facebook': vendor_service_data[7],
            'social_media_instagram': vendor_service_data[8],
            'website_url': vendor_service_data[9],
            'whatsapp': vendor_service_data[10],
            'org_history': vendor_service_data[11],
            'org_location_details': vendor_service_data[12],
            'org_previous_work_details': vendor_service_data[13],
            'org_top_work_details': vendor_service_data[14],
            'org_available_services': vendor_service_data[15],
            'org_best_sites': vendor_service_data[16],
            'award_affiliation': vendor_service_data[17],
            'office_start_time': vendor_service_data[18],
            'office_closed_time': vendor_service_data[19],
            'office_holiday': vendor_service_data[20],
            'office_break_time': vendor_service_data[21],
            'offering_venue': vendor_service_data[22],
            'ceremony_type': vendor_service_data[23],
            'offering_service': vendor_service_data[24],
            'others': vendor_service_data[25],
            'vendor_service_status': vendor_service_data[26]
            }
            return jsonify({
                'success': True,
                'message': f'Profile for Vendor ID {vendor_id} viewed successfully',
                'data': {
                    'vendor_profile': formatted_profile,
                    'vendor_service': formatted_service
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'No profile or service found for Vendor ID {vendor_id}',
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

#----------------------------------  Topics : user service create API Code, Author: Md. Iquball Hossain, Date: 24-12-2023 ---------------------

def create_user_service_form(current_user, vendor_id):
    try:
        if not current_user or 'user_id' not in current_user:
            return jsonify({'success': False, 'message': 'Invalid user token provided.'}), 401
        user_id = current_user['user_id']
        first_name = request.json.get('first_name') 
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        phone = request.json.get('phone')
        ceremony_date = request.json.get('ceremony_date')
        ceremony_time = request.json.get('ceremony_time')
        program_duration = request.json.get('program_duration')
        number_of_guest = request.json.get('number_of_guest')
        about_ceremony = request.json.get('about_ceremony')
        wanted_service = request.json.get('wanted_service')
        wanted_venues = request.json.get('wanted_venues')
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO services.user_service (user_id, vendor_id, first_name, last_name, email, phone, ceremony_date, ceremony_time,
            program_duration, number_of_guest, about_ceremony, wanted_service, wanted_venues, request_status, request_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, vendor_id, first_name, last_name, email, phone, ceremony_date, ceremony_time, program_duration,
            number_of_guest, about_ceremony, wanted_service, wanted_venues, False, datetime.now()))
        connection.commit()
        cursor.close()
        conn.putconn(connection)
        return jsonify({'success': True, 'message': 'User service created successfully.'}), 201
    except Exception as e:
        connection.rollback()
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e), 'request_status': False}), 500
