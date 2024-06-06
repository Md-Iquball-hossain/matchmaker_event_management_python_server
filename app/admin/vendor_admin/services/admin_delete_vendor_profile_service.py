
from flask import Blueprint, jsonify, request
import psycopg2
from app.database import conn

admin_delete_vendor_profile_service = Blueprint("admin_delete_vendor_profile_service", __name__)  

#---------------------  Topics : Admin edit vendor profile (delete) API service , Author: Md. Iquball Hossain, Date: 12-12-2023 (updated 03-12-2023)----------- 

def admin_update_vendor_profile(current_admin,vendor_id):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view user profiles.',
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        new_status = request.form.get('vendor_profile_status')
        new_org_name = request.form.get('org_name')
        if new_org_name:
            update_org_query = "UPDATE vendors.vendor SET org_name = %s WHERE id = %s"
            cursor.execute(update_org_query, (new_org_name, vendor_id))
            connection.commit()
        update_status_query = "UPDATE vendors.vendor SET vendor_profile_status = %s WHERE id = %s"
        cursor.execute(update_status_query, (new_status, vendor_id))
        connection.commit()
        cursor.execute("SELECT org_name, vendor_profile_status FROM vendors.vendor WHERE id = %s", (vendor_id,))
        updated_profile = cursor.fetchone()
        updated_profile_dict = {
            'org_name': updated_profile[0],
            'vendor_profile_status': updated_profile[1]
        }
        return jsonify({
            'success': True,
            'message': 'Vendor profile status and org_name updated successfully',
            'data': updated_profile_dict
        }), 200
    except psycopg2.Error as e:
        return jsonify({
            'success': False,
            'message': f'Database error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500
    finally:
        cursor.close()
        connection.close()

#-----------  Topics : Admin delete vendor profile delete (delete) API service , Author: Md. Iquball Hossain, Date: 28-11-2023 (updated 03-12-2023) -------- 

def delete_vendor_profile(current_admin,vendor_id):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view user profiles.',
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        if not vendor_id:
            return jsonify({
                'success': False,
                'message': 'Vendor ID is missing or invalid.'
            }), 400
        cursor.execute("SELECT * FROM vendors.vendor WHERE id = %s", (vendor_id,))
        vendor_data = cursor.fetchone()
        if not vendor_data:
            return jsonify({
                'success': False,
                'message': 'Vendor profile not found.'
            }), 404
        delete_query = "DELETE FROM vendors.vendor WHERE id = %s"
        cursor.execute(delete_query, (vendor_id,))
        connection.commit()
        cursor.close()
        return jsonify({
            'success': True,
            'message': f'Deleted vendor successfully whose registation id is  {vendor_id} ',
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': f'An error occurred while deleting the vendor profile: {str(e)}'
        }), 500
    finally:
        conn.putconn(connection)