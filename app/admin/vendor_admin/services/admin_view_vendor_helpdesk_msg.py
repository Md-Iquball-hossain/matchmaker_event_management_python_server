
from flask import Blueprint,jsonify
from app.database import conn

admin_vendor_helpdesk_message_view = Blueprint("admin_vendor_helpdesk_message_view", __name__)

#------------ Topics : Admin view vendor's helpdesk all message routes list services, Author: Md. Iquball Hossain, Date: 05-12-2023 ----------

def get_helpdesk_messages(current_admin):
    try:
        if not current_admin or 'admin_id' not in current_admin:
            return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
        connection = conn.getconn()
        cursor = connection.cursor()
        query = """
            SELECT helpdesk_id, vendor_id, problem_topics, problem_file, message_time, problem_status
            FROM vendors.helpdesk
            ORDER BY message_time DESC
        """
        cursor.execute(query)
        helpdesk_messages = cursor.fetchall()
        pending_messages = []
        inprogress_messages = []
        solved_messages = []
        for message in helpdesk_messages:
            helpdesk_id, vendor_id, problem_topics, problem_file, message_time, problem_status = message
            msg_date = message_time.strftime("%Y-%m-%d")
            msg_time = message_time.strftime("%I:%M %p")
            formatted_message = {
                'helpdesk_id': helpdesk_id,
                'vendor_id': vendor_id,
                'problem_topics': problem_topics,
                'problem_file': problem_file,
                'message_date': msg_date,
                'message_time': msg_time,
                'problem_status': problem_status
            }
            if problem_status == 'pending':
                pending_messages.append(formatted_message)
            elif problem_status == 'inprogress':
                inprogress_messages.append(formatted_message)
            elif problem_status == 'solved':
                solved_messages.append(formatted_message)
        cursor.close()
        conn.putconn(connection)
        formatted_messages = pending_messages + inprogress_messages + solved_messages
        return jsonify({
            'success': True,
            'data': formatted_messages
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': 'Failed to fetch helpdesk messages. Please check server logs for more information.'
        }), 500

#------------ Topics : Admin edit vendor's helpdesk message status list services, Author: Md. Iquball Hossain, Date: 14-12-2023 ----------

def edit_helpdesk_status(current_admin, helpdesk_id, new_status):
    allowed_statuses = ['pending', 'inprogress', 'solved']
    try:
        if not current_admin or 'admin_id' not in current_admin:
            return jsonify({'success': False, 'message': 'Invalid admin details provided.'}), 400
        if new_status not in allowed_statuses:
            return jsonify({
                'success': False,
                'message': f"Invalid status. Allowed statuses are: {', '.join(allowed_statuses)}"
            }), 400
        connection = conn.getconn()
        cursor = connection.cursor()
        update_query = """
            UPDATE vendors.helpdesk
            SET problem_status = %s
            WHERE helpdesk_id = %s
        """
        cursor.execute(update_query, (new_status, helpdesk_id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({
            'success': True,
            'message': f'Helpdesk message status updated to {new_status} for ID {helpdesk_id} successfully.'
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': 'Failed to update helpdesk message status.'
        }), 500