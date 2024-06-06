from flask import jsonify
from flask import Blueprint, jsonify
from app.database import conn
import datetime

admin_vendor_service = Blueprint('admin_vendor_service', __name__)

#----------------------------------  Topics : Admin view vendor service list API Code, Author: Md. Iquball Hossain, Date: 21-12-2023 ------------------------

def admin_view_vendor_service(current_admin):
    if not current_admin or 'admin_id' not in current_admin:
        return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
    try:
        if current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view vendor service.'
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        admin_id = current_admin.get('admin_id')
        query = "SELECT * FROM vendors.vendor_service WHERE admin_id = %s"
        cursor.execute(query, (admin_id,))
        vendor_service_data = cursor.fetchall()
        if not vendor_service_data:
            return jsonify({'success': False, 'message': 'No vendor service data found for this admin ID.'}), 404
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
                'vendor_service_status': row[26],
                'office_start_time': row[18],
                'office_closed_time' : row[19]
            }
            created_at = row[27] 
            last_edited = row[28]
            if isinstance(last_edited, datetime.datetime):
                formatted_row['last_edited'] = last_edited.strftime('%Y-%m-%d %I:%M %p')
            else:
                formatted_row['last_edited'] = last_edited
            if isinstance(created_at, datetime.datetime):
                formatted_row['created_at'] = created_at.strftime('%Y-%m-%d %I:%M %p')
            else:
                formatted_row['created_at'] = created_at
            formatted_data.append(formatted_row)
        return jsonify({"data": formatted_data})
    except Exception as e:
        if 'conn' in locals():
            conn.rollback() 
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()
        conn.putconn(connection)
        cursor.close()

#----------------------------------  Topics : Admin view vendor single service from list API Code, Author: Md. Iquball Hossain, Date: 21-12-2023 ------------------------

def admin_view_single_vendor_service(current_admin, vendor_service_id):
    if not current_admin or 'admin_id' not in current_admin:
        return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
    try:
        if current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view vendor service.'
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vendors.vendor_service WHERE vendor_service_id = %s", (vendor_service_id,))
        vendor_service_data = cursor.fetchone()
        if not vendor_service_data:
            return jsonify({'success': False, 'message': 'No vendor service found for this ID.'}), 404
        vendor_id = vendor_service_data[1]  
        cursor.execute("SELECT * FROM vendors.vendor WHERE id = %s", (vendor_id,))
        vendor_profile = cursor.fetchone()
        if not vendor_profile:
            return jsonify({'success': False, 'message': 'No vendor found for this ID.'}), 404
        formatted_row = {
            'vendor_reg_id': vendor_profile[0],
            'org_name': vendor_profile[1],
            'org_username': vendor_profile[2],
            'email': vendor_profile[3],
            'phone_number': vendor_profile[5],
            'photo': vendor_profile[6],
            'address': vendor_profile[7],
            'city': vendor_profile[8],
            'country': vendor_profile[9],
            'details': vendor_profile[11],
            'created_at': str(vendor_profile[12]),
            'last_login_at': str(vendor_profile[13]),
            'vendor_status': vendor_profile[14],
            'vendor_profile_status': vendor_profile[15],
            'tin_certificate': vendor_profile[16],
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
        office_start_time = vendor_service_data[18]
        office_closed_time = vendor_service_data[19]
        created_at = vendor_service_data[27]
        last_edited = vendor_service_data[28]
        formatted_row['office_start_time'] = office_start_time.strftime('%I:%M:%S') if isinstance(office_start_time, datetime.time) else office_start_time
        formatted_row['office_closed_time'] = office_closed_time.strftime('%I:%M:%S') if isinstance(office_closed_time, datetime.time) else office_closed_time
        formatted_row['created_at'] = created_at.strftime('%Y-%m-%d %I:%M %p') if isinstance(created_at, datetime.datetime) else created_at
        formatted_row['last_edited'] = last_edited.strftime('%Y-%m-%d %I:%M %p') if isinstance(last_edited, datetime.datetime) else last_edited
        return jsonify({"data": formatted_row})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
        conn.putconn(connection)

#----------------------------------  Topics : Admin view vendor single service from list API Code, Author: Md. Iquball Hossain, Date: 21-12-2023 ------------------------

def admin_change_vendor_service_permission(current_admin, vendor_service_id):
    try:
        if not current_admin or 'admin_id' not in current_admin:
            return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT vendor_service_status FROM vendors.vendor_service WHERE vendor_service_id = %s", (vendor_service_id,))
        current_status = cursor.fetchone()
        if not current_status:
            return jsonify({'success': False, 'message': 'No vendor service found for this ID.'}), 404
        new_status = not current_status[0]
        cursor.execute("UPDATE vendors.vendor_service SET vendor_service_status = %s WHERE vendor_service_id = %s", (new_status, vendor_service_id))
        connection.commit()
        return jsonify({'success': True, 'message': f"Vendor service status updated to {new_status}."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
        conn.putconn(connection)
