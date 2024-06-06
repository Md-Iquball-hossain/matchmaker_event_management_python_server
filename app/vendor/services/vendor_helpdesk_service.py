import datetime
from flask import Blueprint, jsonify, request
from utils.s3_bucket.s3_bucket import Uploader
from app.database import conn

vendor_notice_view_service = Blueprint('vendor_notice_view_service', __name__)

#----------------------------------  Topics : create helpdesk message from API service, Author: Md. Iquball Hossain, Date: 30-11-2023 ------------------------------------

def create_helpdesk_message(current_vendor):
    try:
        vendor_id = current_vendor.get('id')
        if not vendor_id:
            return jsonify({
                'success': False,
                'message': 'Vendor ID is missing.'
            }), 400
        data = request.form.to_dict()
        problem_topics = data.get('problem_topics')
        file = request.files.get('problem_file')
        if not problem_topics and not file:
            return jsonify({
                'success': False,
                'message': 'Either Problem Topics or Problem File is required.'
            }), 400
        problem_file_path = None
        if file:
            success, file_path = Uploader.cloudUpload(file, "helpdesk_files")
            if success:
                problem_file_path = file_path
        connection = conn.getconn()
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO vendors.helpdesk (vendor_id, problem_topics, problem_file, problem_status)
            VALUES (%s, %s, %s, 'pending') RETURNING helpdesk_id, message_time
        """
        cursor.execute(insert_query, (vendor_id, problem_topics, problem_file_path))
        inserted_data = cursor.fetchone()
        helpdesk_id, message_time = inserted_data
        connection.commit()
        cursor.close()
        connection.close()
        formatted_date = message_time.strftime("%Y-%m-%d")
        formatted_time = message_time.strftime("%I:%M %p")
        return jsonify({
            'success': True,
            'message': 'Helpdesk message created successfully',
            'data': {
                'helpdesk_id': helpdesk_id,
                'vendor_id': vendor_id,
                'problem_topics': problem_topics,
                'problem_file_path': problem_file_path,
                'problem_status': 'pending',
                'message_date': formatted_date,
                'message_time': formatted_time
            }
        }), 201
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': 'Failed to create helpdesk message'
        }), 500
    finally:
        connection.close()
        conn.putconn(connection)
        cursor.close()

#----------------------------------  Topics : view helpdesk message from API service, Author: Md. Iquball Hossain, Date: 30-11-2023 -------------------------------------

def get_vendor_helpdesk_messages(current_vendor):
    try:
        vendor_id = current_vendor.get('id')
        if not vendor_id:
            return jsonify({
                'success': False,
                'message': 'Vendor ID is missing.'
            }), 400
        connection = conn.getconn()
        cursor = connection.cursor()
        select_query = """
            SELECT helpdesk_id, problem_topics, problem_file, problem_status, message_time
            FROM vendors.helpdesk
            WHERE vendor_id = %s
        """
        cursor.execute(select_query, (vendor_id,))
        helpdesk_messages = cursor.fetchall()
        cursor.close()
        connection.close()
        formatted_messages = []
        for message in helpdesk_messages:
            helpdesk_id, problem_topics, problem_file, problem_status, message_time = message
            msg_date = message_time.strftime("%Y-%m-%d")
            msg_time = message_time.strftime("%I:%M %p")
            formatted_messages.append({
                'helpdesk_id': helpdesk_id,
                'problem_topics': problem_topics,
                'problem_file': problem_file,
                'problem_status': problem_status,
                'message_date': msg_date,
                'message_time': msg_time
            })
        return jsonify({
            'success': True,
            'data': formatted_messages
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': 'Failed to fetch helpdesk messages for the vendor'
        }), 500

#----------------------------------  Topics : edit helpdesk message from API service, Author: Md. Iquball Hossain, Date: 30-11-2023 -------------------------------------

def update_helpdesk_message(current_vendor):
    try:
        vendor_id = current_vendor.get('id')
        if not vendor_id:
            return jsonify({
                'success': False,
                'message': 'Vendor ID is missing.'
            }), 400
        data = request.form.to_dict()
        helpdesk_id = request.args.get('helpdesk_id')
        if not helpdesk_id:
            return jsonify({
                'success': False,
                'message': 'Helpdesk ID is missing in the request.'
            }), 400
        problem_topics = data.get('problem_topics')
        file = request.files.get('problem_file')
        problem_file_path = None
        if file:
            success, file_path = Uploader.cloudUpload(file, "helpdesk_files")
            if success:
                problem_file_path = file_path
        connection = conn.getconn()
        cursor = connection.cursor()
        select_query = """
            SELECT vendor_id FROM vendors.helpdesk WHERE helpdesk_id = %s
        """
        cursor.execute(select_query, (helpdesk_id,))
        row = cursor.fetchone()
        if not row or row[0] != vendor_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized to edit this helpdesk message'
            }), 403 
        update_query = """
            UPDATE vendors.helpdesk
            SET problem_topics = %s, problem_file = %s, last_edited = CURRENT_TIMESTAMP
            WHERE helpdesk_id = %s
            RETURNING helpdesk_id, message_time
        """
        cursor.execute(update_query, (problem_topics, problem_file_path, helpdesk_id))
        updated_data = cursor.fetchone()
        helpdesk_id, message_time = updated_data
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({
            'success': True,
            'message': 'Helpdesk message updated successfully',
            'data': {
                'helpdesk_id': helpdesk_id,
                'vendor_id': vendor_id,
                'problem_topics': problem_topics,
                'problem_file_path': problem_file_path,
                'message_time': message_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': 'Failed to update helpdesk message'
        }), 500


