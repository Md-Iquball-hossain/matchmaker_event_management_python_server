#----------------------------------  Topics : vendor profile All API service, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

from flask import Blueprint, jsonify, request
from app.database import conn
from utils.lib.lib import hash_password
from utils.s3_bucket.s3_bucket import Uploader
import psycopg2
from utils.miscellaneous.status_code import status_code

vendor_profile = Blueprint('vendor_profile', __name__)

#----------------------------------  Topics : vendor profile view (get) API service, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

def view_vendor_profile(current_vendor):
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
        vendor_profile = {
            'vendor_reg_num': vendor_data[0],
            'org_name': vendor_data[1] if vendor_data[1] else '',
            'org_username': vendor_data[2] if vendor_data[2] else '',
            'email': vendor_data[3] if vendor_data[3] else '',
            'password': vendor_data[4] if vendor_data[4] else '',
            'phone_number': vendor_data[5] if vendor_data[5] else '',
            'photo': vendor_data[6] if vendor_data[6] else '',
            'address': vendor_data[7] if vendor_data[7] else '',
            'city': vendor_data[8] if vendor_data[8] else '',
            'country': vendor_data[9] if vendor_data[9] else '',
            'business_category': vendor_data[10] if vendor_data[10] else '',
            'details': str(vendor_data[11]) if vendor_data[11] else '',
            'Vendor_profile_status': vendor_data[15] if vendor_data[15] else '',
            'last_login': vendor_data[13] if vendor_data[13] else '',
            'vendor_status': vendor_data[14] if vendor_data[14] else '',
            'vendor_profile_created': str(vendor_data[12]) if vendor_data[12] else '',
            'tin_certificate': vendor_data[16] if vendor_data[16] else '',
        }
        cursor.close()
        return jsonify({
            'success': True,
            'message': 'Vendor profile view successful',
            'data': vendor_profile
        }), 200
    except psycopg2.Error as e:
        print(e)
        return jsonify({
            'success': False,
            'message': 'Failed to fetch vendor profile.'
        }), 500
    finally:
        conn.putconn(connection)

#----------------------------------  Topics : vendor profile edit/update (put) API service, Author: Md. Iquball Hossain, Date: 27-11-2023 -------------------------------------

def update_vendor_profile(current_vendor):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        vendor_id = current_vendor.get('id')
        if not vendor_id:
            return jsonify({
                'success': False,
                'message': 'Vendor ID is missing.'
            }), status_code['HTTP_BAD_REQUEST']
        data = request.form.to_dict()
        file_photo = request.files.get('photo')
        file_tin_certificate = request.files.get('tin_certificate')
        if not data and not file_photo and not file_tin_certificate:
            return jsonify({
                'success': False,
                'message': 'No data provided for update',
            }), status_code['HTTP_BAD_REQUEST']
        update_values = {}
        if file_photo:
            success_photo, key_photo = Uploader.cloudUpload(file_photo, "vendor_photos")
            if success_photo:
                update_values['photo'] = key_photo
        tin_certificate = None
        if file_tin_certificate:
            success_tin_cert, key_tin_cert = Uploader.cloudUpload(file_tin_certificate, "tin_certificates")
            if success_tin_cert:
                tin_certificate = key_tin_cert
                update_values['tin_certificate'] = tin_certificate
        update_values.update({k: v for k, v in data.items() if k != 'id'})
        if not update_values:
            return jsonify({
                'success': False,
                'message': 'No valid fields provided for update',
            }), status_code['HTTP_BAD_REQUEST']
        if 'password' in update_values:
            password = update_values.pop('password') 
            hashed_password = hash_password(password)
            update_values['password_hash'] = hashed_password
        update_query = "UPDATE vendors.vendor SET "
        update_query += ', '.join([f"{key} = %s" for key in update_values.keys()])
        update_query += " WHERE id = %s"
        update_values['id'] = vendor_id
        cursor.execute(update_query, tuple(update_values.values()))
        connection.commit()
        cursor.execute("SELECT * FROM vendors.vendor WHERE id = %s", (vendor_id,))
        updated_profile = cursor.fetchone()
        updated_profile_dict = {
            'vendor_reg_num': updated_profile[0],
            'org_name': updated_profile[1],
            'org_username': updated_profile[2],
            'email': updated_profile[3],
            'password': updated_profile[4],
            'phone_number': updated_profile[5],
            'photo': updated_profile[6],
            'address': updated_profile[7],
            'city': updated_profile[8],
            'country': updated_profile[9],
            'business_category': updated_profile[10],
            'Details': updated_profile[11],
            'profile_created': updated_profile[12], 
            'tin_certificate': updated_profile[16], 
            'last_login': updated_profile[13]
        }
        return jsonify({
            'success': True,
            'message': 'Vendor profile updated successfully',
            'data': updated_profile_dict
        }), status_code['HTTP_OK']
    except KeyError as key_error:
        return jsonify({
            'success': False,
            'message': f"Missing key in request data: {str(key_error)}",
        }), status_code['HTTP_BAD_REQUEST']
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': f'An error occurred while processing the request: {str(e)}',
        }), status_code['HTTP_INTERNAL_SERVER_ERROR']
    finally:
        connection.close()
        conn.putconn(connection)
        cursor.close()

#----------------------------------  Topics : vendor profile delete (delete) API service , Author: Md. Iquball Hossain, Date: 28-11-2023 ------------------------------------- 

def delete_vendor_profile(current_vendor):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        vendor_id = current_vendor.get('id')
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
        deleted_id = vendor_id 
        cursor.close()
        return jsonify({
            'success': True,
            'message': 'Vendor profile deleted successfully',
            'vendor_reg_num': deleted_id
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': f'An error occurred while deleting the vendor profile: {str(e)}'
        }), 500
    finally:
        connection.close()
        conn.putconn(connection)
        cursor.close()

