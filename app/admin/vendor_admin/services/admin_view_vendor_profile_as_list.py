from datetime import datetime
from flask import Blueprint,jsonify
from app.database import conn
from utils.miscellaneous.status_code import status_code

admin_vendor_profile_list_service = Blueprint("admin_vendor_profile_list_service", __name__)

#-------------------------  Topics : Admin vendor all profile list services, Author: Md. Iquball Hossain, Date: 03-12-2023 ----------------

def get_all_vendor_profiles(current_admin):
    try:
        if current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can create a new admin profile.',
            }), status_code['HTTP_FORBIDDEN']
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vendors.vendor ORDER BY created_at DESC")
        profiles = cursor.fetchall()
        cursor.close()
        conn.putconn(connection)
        formatted_profiles = []
        for profile in profiles:
            formatted_profiles.append({
                'vendor_reg_id': profile[0],
                'org_name': profile[1],
                'org_username': profile[2],
                'email': profile[3],
                'phone_number': profile[5],
                'photo': profile[6],
                'address': profile[7],
                'city': profile[8],
                'country': profile[9],
                'business_category': profile[10],
                'details': profile[11],
                'created_at': str(profile[12]),
                'last_login_at': str(profile[13]),
                'vendor_status': profile[14],
                'vendor_profile_status': profile[15],
                'tin_certificate': profile[16]
            })
        total_profiles = len(profiles)
        formatted_profiles.append({
            'total_profiles': total_profiles
        })
        return jsonify({
            'success': True,
            'message': 'All vendor profiles view successfully',
            'data': formatted_profiles
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

#----------------------  Topics : Admin vendor single profile list routes, Author: Md. Iquball Hossain, Date: 03-12-2023 ---------------------

def get_vendor_single_profile(current_admin, vendor_id):
    try:
        if not current_admin or 'admin_id' not in current_admin:
            return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
        
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vendors.vendor WHERE id = %s", (vendor_id,))
        vendor_profile = cursor.fetchone()
        cursor.execute("SELECT * FROM vendors.vendor ORDER BY created_at DESC")
        all_profiles = cursor.fetchall()
        cursor.close()
        conn.putconn(connection)
        if vendor_profile:
            created_at = vendor_profile[12]
            last_login_at = vendor_profile[13]
            
            formatted_created_at_date = formatted_created_at_time = formatted_last_login_at_date = formatted_last_login_at_time = None
            
            if created_at:
                formatted_created_at_date = created_at.strftime("%d-%m-%Y")
                formatted_created_at_time = created_at.strftime("%I:%M %p")
            if last_login_at:
                formatted_last_login_at_date = last_login_at.strftime("%d-%m-%Y")
                formatted_last_login_at_time = last_login_at.strftime("%I:%M %p")
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
                'vendor_status': vendor_profile[14],
                'vendor_profile_status': vendor_profile[15],
                'tin_certificate': vendor_profile[16],
                'created_date': formatted_created_at_date,
                'created_time': formatted_created_at_time,
                'last_login_at_date': formatted_last_login_at_date,
                'last_login_at_time': formatted_last_login_at_time
            }
            total_profiles = len(all_profiles)
            return jsonify({
                'success': True,
                'message': f'Profile for Vendor ID {vendor_id} viewed successfully',
                'data': formatted_profile,
                'total_profiles': total_profiles
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'No profile found for Vendor ID {vendor_id}',
                'total_profiles': len(all_profiles)
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

#-----------------  Topics : Admin vendor single profile list by busness category routes, Author: Md. Iquball Hossain, Date: 03-12-2023 --------------

ALLOWED_CATEGORY = ['Photography', 'Catering', 'Music Band', 'Outdoor venue', 'Indoor Venue','Cake', 'Beauty and Makeup']

def get_profiles_by_business_category(current_admin, business_category):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view profiles by business category.',
            }), 403
        if business_category not in ALLOWED_CATEGORY:
            return jsonify({
                'success': False,
                'message': f'Invalid business category. Allowed categories are: {", ".join(ALLOWED_CATEGORY)}',
            }), 400
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vendors.vendor WHERE business_category = %s ORDER BY created_at DESC", (business_category,))
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
                'business_category': profile[10],
                'details': profile[11],
                'created_at': str(profile[12]),
                'last_login_at': str(profile[13]),
                'vendor_status': profile[14],
                'vendor_profile_status': profile[15],
                'tin_certificate': profile[16]
            }
            formatted_profiles.append(formatted_profile)
        return jsonify({
            'success': True,
            'message': f'Profiles for business category {business_category} viewed successfully',
            'data': formatted_profiles
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

#-----------------  Topics : Admin vendor single profile list by busness category routes, Author: Md. Iquball Hossain, Date: 03-12-2023 -------------

ALLOWED_CATEGORIES = ['pending', 'verified', 'blocked']

def get_pending_vendor_profiles(current_admin, vendor_profile_status):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view profiles by business category.',
            }), 403
        if vendor_profile_status not in ALLOWED_CATEGORIES:
            return jsonify({
                'success': False,
                'message': f'Invalid vendor profile status. Allowed categories are: {", ".join(ALLOWED_CATEGORIES)}',
            }), 400
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vendors.vendor WHERE vendor_profile_status = %s ORDER BY created_at DESC", (vendor_profile_status,))
        profiles = cursor.fetchall()
        cursor.close()
        conn.putconn(connection)
        if not profiles:
            return jsonify({
                'success': False,
                'message': f'No profiles found for vendor profile status {vendor_profile_status}',
            }), 404
        formatted_profiles = []
        for profile in profiles:
            formatted_profiles.append({
                'vendor_reg_id': profile[0],
                'org_name': profile[1],
                'org_username': profile[2],
                'email': profile[3],
                'phone_number': profile[5],
                'photo': profile[6],
                'address': profile[7],
                'city': profile[8],
                'country': profile[9],
                'business_category': profile[10],
                'details': profile[11],
                'created_at': str(profile[12]),
                'last_login_at': str(profile[13]),
                'vendor_status': profile[14],
                'vendor_profile_status': profile[15],
                'tin_certificate': profile[16]
            })
        return jsonify({
            'success': True,
            'message': 'All pending vendor profiles viewed successfully',
            'data': formatted_profiles
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500
