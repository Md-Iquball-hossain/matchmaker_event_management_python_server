from flask import request, jsonify
from flask import Blueprint, jsonify, request
from utils.s3_bucket.s3_bucket import Uploader
from app.database import conn
from datetime import datetime, time

vendor_service = Blueprint('vendor_service', __name__)

#----------------------------------  Topics : vendor create service form API Code, Author: Md. Iquball Hossain, Date: 17-12-2023 ------------------------

def create_vendor_service(current_vendor):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        vendor_id = current_vendor.get('id')
        if not vendor_id:
            return jsonify({
                'success': False,
                'message': 'Vendor ID is missing.'
            }), 400
        query = "SELECT * FROM vendors.vendor WHERE id = %s"
        cursor.execute(query, (vendor_id,))
        vendor_data = cursor.fetchone()
        if not vendor_data:
            return jsonify({
                'success': False,
                'message': 'Vendor profile not found.'
            }), 404
        data = request.form.to_dict()
        admin_id = data.get('admin_id')
        admin_id = data.get('admin_id')
        admin_query = "SELECT * FROM admin.admin_profile WHERE admin_id = %s"
        cursor.execute(admin_query, (admin_id,))
        admin_data = cursor.fetchone()
        if not admin_data:
            return jsonify({
                'success': False,
                'message': 'Admin ID does not exist. Please provide a valid admin ID.'
            }), 400
        business_category_name = data.get('business_category_name')
        business_type = data.get('business_type')
        guest_capacity = data.get('guest_capacity')
        pricing_file = data.get('pricing_file')
        pricing_file = None
        file = request.files.get('pricing_file')
        if file:
            success, file_path = Uploader.cloudUpload(file, "s3_bucket")
            if success:
                pricing_file = file_path
            else:
                return jsonify({
                    'success': False,
                    'message': 'File upload failed.'
                }), 500
        social_media_facebook = data.get('social_media_facebook')
        social_media_instagram = data.get('social_media_instagram')
        website_url = data.get('website_url')
        whatsapp = data.get('whatsapp')
        org_history = data.get('org_history')
        org_location_details = data.get('org_location_details')
        org_previous_work_details = data.get('org_previous_work_details')
        org_top_work_details = data.get('org_top_work_details')
        org_available_services = data.get('org_available_services')
        org_best_sites = data.get('org_best_sites')
        award_affiliation = data.get('award_affiliation')
        office_start_time = data.get('office_start_time')
        office_closed_time = data.get('office_closed_time')
        office_holiday = data.get('office_holiday')
        office_break_time = data.get('office_break_time')
        offering_venue = data.get('offering_venue')
        ceremony_type = data.get('ceremony_type')
        offering_service = data.get('offering_service')
        others = data.get('others')
        cursor.execute(
            '''
            INSERT INTO vendors.vendor_service (
                vendor_id,
                admin_id,
                business_category_name,
                business_type,
                guest_capacity,
                pricing_file,
                social_media_facebook,
                social_media_instagram,
                website_url,
                whatsapp,
                org_history,
                org_location_details,
                org_previous_work_details,
                org_top_work_details,
                org_available_services,
                org_best_sites,
                award_affiliation,
                office_start_time,
                office_closed_time,
                office_holiday,
                office_break_time,
                offering_venue,
                ceremony_type,
                offering_service,
                others,
                vendor_service_status,
                created_time,
                last_edited_time
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, NOW(), NOW()
            )
            ''',
            (
                vendor_id,
                admin_id,
                business_category_name,
                business_type,
                guest_capacity,
                pricing_file,
                social_media_facebook,
                social_media_instagram,
                website_url,
                whatsapp,
                org_history,
                org_location_details,
                org_previous_work_details,
                org_top_work_details,
                org_available_services,
                org_best_sites,
                award_affiliation,
                office_start_time,
                office_closed_time,
                office_holiday,
                office_break_time,
                offering_venue,
                ceremony_type,
                offering_service,
                others,
                False
            )
        )
        connection.commit()
        return jsonify({"message": "Vendor service created successfully"})
    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            conn.putconn(connection)

#----------------------------------  Topics : Vendor view service list API Code, Author: Md. Iquball Hossain, Date: 20-12-2023 ------------------------

def get_vendor_service(current_vendor):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        vendor_id = current_vendor.get('id')
        if not vendor_id:
            return jsonify({'success': False, 'message': 'Vendor ID is missing.'}), 400
        query = "SELECT * FROM vendors.vendor_service WHERE vendor_id = %s ORDER BY vendor_service_id DESC LIMIT 1"
        cursor.execute(query, (vendor_id,))
        vendor_service_data = cursor.fetchall()
        if not vendor_service_data:
            return jsonify({'success': False, 'message': 'No vendor service data found for this vendor ID.'}), 404
        formatted_data = []
        for row in vendor_service_data:
            formatted_row = {
                'vendor_service_id': row[0],
                'vendor_id': row[1],
                'admin_id': row[2],
                'business_category_name': row[3],
                'business_type': row[4],
                'guest_capacity': row[5],
                'pricing_file': row[6],
                'social_media_facebook': row[7],
                'social_media_instagram': row[8],
                'website_url': row[9],
                'whatsapp': row[10],
                'org_history': row[11],
                'org_location_details': row[12],
                'org_previous_work_details': row[13],
                'org_top_work_details': row[14],
                'org_available_services': row[15],
                'org_best_sites': row[16],
                'award_affiliation': row[17],
                'office_holiday': row[20],
                'office_break_time': row[21],
                'offering_venue': row[22],
                'ceremony_type': row[23],
                'offering_service': row[24],
                'others': row[25],
                'vendor_service_status': row[26]
            }
            office_start_time = row[18]
            office_closed_time = row[19]
            created_at = row[27] 
            last_edited = row[28]
            formatted_row['last_edited'] = last_edited.strftime('%Y-%m-%d %I:%M %p') if isinstance(last_edited, datetime) else last_edited
            formatted_row['created_at'] = created_at.strftime('%Y-%m-%d %I:%M %p') if isinstance(created_at, datetime) else created_at
            formatted_row['office_start_time'] = office_start_time.strftime('%I:%M:%S') if isinstance(office_start_time, time) else office_start_time
            formatted_row['office_closed_time'] = office_closed_time.strftime('%I:%M:%S') if isinstance(office_closed_time, time) else office_closed_time
            formatted_data.append(formatted_row)
        return jsonify({"data": formatted_data})
    except Exception as e:
        if 'conn' in locals():
            conn.rollback() 
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                conn.putconn(connection)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

#----------------------------------  Topics : Edit Vendor service API Code, Author: Md. Iquball Hossain, Date: 20-12-2023 ------------------------

def edit_vendor_service(current_vendor):
    try:
        vendor_id = current_vendor.get('id')
        connection = conn.getconn()
        cursor = connection.cursor()
        query = "SELECT * FROM vendors.vendor_service WHERE vendor_id = %s ORDER BY vendor_service_id DESC LIMIT 1"
        cursor.execute(query, (vendor_id,))
        vendor_service_data = cursor.fetchone()
        if not vendor_service_data:
            return jsonify({'success': False, 'message': 'No vendor service data found for this vendor ID.'}), 404
        pricing_file = None
        file = request.files.get('pricing_file')
        if file:
            uploader = Uploader() 
            success, file_path = uploader.cloudUpload(file)
            if success:
                pricing_file = file_path
        update_query = "UPDATE vendors.vendor_service SET "
        update_values = []
        fields_in_database_order = [
            'admin_id',
            'business_category_name',
            'business_type',
            'guest_capacity',
            'pricing_file',
            'social_media_facebook',
            'social_media_instagram',
            'website_url',
            'whatsapp',
            'org_history',
            'org_location_details',
            'org_previous_work_details',
            'org_top_work_details',
            'org_available_services',
            'org_best_sites',
            'award_affiliation',
            'office_start_time',
            'office_closed_time',
            'office_holiday',
            'office_break_time',
            'offering_venue',
            'ceremony_type',
            'offering_service',
            'others',
        ]
        for field in fields_in_database_order:
            value = request.form.get(field)
            if value is not None:
                if field == 'pricing_file':
                    update_query += f"{field} = %s, "
                    update_values.append(pricing_file)
                else:
                    if field in ['office_start_time', 'office_closed_time']:
                        update_query += f"{field} = %s, "
                        update_values.append(str(value))
                    else:
                        update_query += f"{field} = %s, "
                        update_values.append(value)
        update_query += "last_edited_time = %s, "
        update_values.append(datetime.now()) 
        update_query = update_query[:-2] 
        update_query += " WHERE vendor_id = %s AND vendor_service_id = %s"
        update_values.extend([vendor_id, vendor_service_data[0]])
        cursor.execute(update_query, tuple(update_values))
        cursor.execute("UPDATE vendors.vendor_service SET vendor_service_status = %s WHERE vendor_service_id = %s", (False, vendor_service_data[0]))
        connection.commit()
        return jsonify({"message": "Vendor service updated successfully"})
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            connection.close()
            conn.putconn(connection)
        if 'cursor' in locals():
            cursor.close()

#-------------------  Topics : view user service from vendor dashboard API Code, Author: Md. Iquball Hossain, Date: 24-12-2023 ------------------------

def get_user_service(current_vendor):
    try:
        if not current_vendor or 'id' not in current_vendor:
            return jsonify({'success': False, 'message': 'Invalid vendor token provided.'}), 401
        vendor_id = current_vendor['id']
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM services.user_service WHERE vendor_id = %s ORDER BY user_service_id DESC
        """, (vendor_id,))
        user_services = cursor.fetchall()
        cursor.close()
        conn.putconn(connection)
        formatted_services = []
        for service in user_services:
            formatted_data = {
                'user_service_id': service[0],
                'user_id': service[1],
                'first_name': service[3],
                'last_name': service[4],
                'email': service[5],
                'phone': service[6],
                'ceremony_date': str(service[7]),
                'ceremony_time': service[8],
                'program_duration': service[9],
                'number_of_guest': service[10],
                'about_ceremony': service[11],
                'wanted_service': service[12],
                'wanted_venues': service[13],
                'request_status': service[14],
                'request_time': str(service[15]),
            }
            formatted_services.append(formatted_data)
        return jsonify({
            'success': True,
            'message': f'User services for Vendor ID {vendor_id} fetched successfully',
            'data': formatted_services,
            'total_services': len(user_services)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

#-------------------  Topics : vendor accept user service request API Code, Author: Md. Iquball Hossain, Date: 24-12-2023 ------------------------

def change_user_message_status(current_vendor, user_service_id):
    try:
        if not current_vendor or 'id' not in current_vendor:
            return jsonify({'success': False, 'message': 'Invalid vendor token provided.'}), 401
        vendor_id = current_vendor['id']
        new_status = request.json.get('new_status')
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE services.user_service
            SET request_status = %s
            WHERE user_service_id = %s AND vendor_id = %s
        """, (new_status, user_service_id, vendor_id))
        connection.commit()
        cursor.close()
        conn.putconn(connection)
        return jsonify({'success': True, 'message': 'User message status updated successfully.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

