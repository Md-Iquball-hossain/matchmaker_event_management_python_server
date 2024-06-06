from flask import Blueprint,jsonify, request
from app.database import conn
import psycopg2
from utils.s3_bucket.s3_bucket import Uploader

notice_for_vendor = Blueprint("notice_for_vendor", __name__)

#----------------------------------  Topics : Create notice for vendor by admin, Author: Md. Iquball Hossain, Date: 29-11-2023 -------------------------------------

def create_notice_for_vendor(current_admin):
    try:
        if not current_admin or 'admin_id' not in current_admin:
            return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
        admin_id = current_admin.get('admin_id')
        vendor_identifier = request.form.get('vendor_identifier')
        notice_title = request.form.get('notice_title')
        notice_topics = ', '.join(request.form.getlist('notice_topics')) if request.form.getlist('notice_topics') else ''
        notice_file = request.files.get('notice_file')
        if notice_file:
            success, file_key = Uploader.cloudUpload(notice_file, 's3_bucket_name')
        else:
            success = True
            file_key = None
        if success:
            connection = conn.getconn()
            cursor = connection.cursor()
            if vendor_identifier.isdigit():
                cursor.execute('''
                    INSERT INTO admin.vendor_notice (vendor_id, admin_id, notice_title, notice_topics, notice_file)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (vendor_identifier, admin_id, notice_title, notice_topics, file_key))
                connection.commit()
                cursor.close()
                return jsonify({
                    'success': True,
                    'message': 'Notice created successfully',
                    'admin_id': admin_id,
                    'vendor_reg_id': vendor_identifier,
                    'notice_title': notice_title,
                    'notice_topics': notice_topics,
                    'notice_file': file_key
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid vendor identifier. It should contain only digits.'}), 400
        else:
            return jsonify({'success': False, 'message': 'Failed to upload file to S3'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

#----------------------------------  Topics : admin view all their personal notice, Author: Md. Iquball Hossain, Date: 29-11-2023 -------------------------------------

def get_notices_for_admin(current_admin):
    try:
        if not current_admin or 'admin_id' not in current_admin:
            return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
        admin_id = current_admin['admin_id']
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id, vendor_id, admin_id, notice_title, notice_topics, notice_file, notice_time
            FROM admin.vendor_notice
            WHERE admin_id = %s
        ''', (admin_id,))
        notices = cursor.fetchall()
        notices_list = []
        for notice in notices:
            notice_dict = {
                'id': notice[0],
                'vendor_id': notice[1],
                'admin_id': notice[2],
                'notice_title': notice[3],
                'notice_topics': notice[4],
                'notice_file': notice[5],
                'notice_date': notice[6].strftime('%d-%m-%Y'),
                'notice_time': notice[6].strftime('%I:%M %p') if notice[6] else None
            }
            notices_list.append(notice_dict)
        cursor.close()
        connection.close()
        return jsonify({'success': True, 'data': notices_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

#----------------------------------  Topics : Update notice for vendor by admin, Author: Md. Iquball Hossain, Date: 29-11-2023 -------------------------------------

def update_notice_for_vendor(current_admin,notice_id):
    try:
        if not current_admin or 'admin_id' not in current_admin:
            return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
        notice_title = request.form.get('notice_title')
        notice_topics = ', '.join(request.form.getlist('notice_topics'))
        notice_file = request.files.get('notice_file')
        file_key = None
        if notice_file:
            success, file_key = Uploader.cloudUpload(notice_file, 'notices')
            if not success:
                return jsonify({'success': False, 'message': 'Failed to upload file to S3'}), 500
        notice_topics = notice_topics.strip() if notice_topics else None
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute(
            'SELECT admin.edit_notice_for_vendor(%s, %s, %s, %s)',
            (notice_id, notice_title, notice_topics, file_key)
        )
        connection.commit()
        cursor.execute(
            'SELECT * FROM admin.vendor_notice WHERE id = %s',
            (notice_id,)
        )
        updated_notice = cursor.fetchone()
        cursor.close()
        return jsonify({
            'success': True,
            'message': 'Notice updated successfully',
            'updated_notice': {
                'updated notice id': updated_notice[0],
                'vendor_reg_id': updated_notice[1],
                'notice_title': updated_notice[2],
                'notice_topics': updated_notice[3],
                'notice_file': updated_notice[4],
                'notice_time': updated_notice[5].isoformat() if updated_notice[5] else None
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

#----------------------------------  Topics : Delete notice for vendor by admin, Author: Md. Iquball Hossain, Date: 29-11-2023 -------------------------------------

def delete_notice_for_vendor(current_admin,notice_id):
    try:
        if not current_admin or 'admin_id' not in current_admin:
            return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM admin.vendor_notice WHERE id = %s", (notice_id,))
        connection.commit()
        cursor.close()
        return jsonify({
            'success': True,
            'message': 'Notice deleted successfully',
            'Deleted Notice Id': notice_id
        }), 200
    except psycopg2.Error as e:
        print(e)
        return jsonify({
            'success': False,
            'message': 'Failed to delete notice for the vendor.'
        }), 500
    finally:
        conn.putconn(connection)
