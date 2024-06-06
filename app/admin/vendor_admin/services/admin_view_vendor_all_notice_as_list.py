
#----------------------------------  Topics : Admin view vendor's notice services, Author: Md. Iquball Hossain, Date: 03-12-2023 ----------------

from flask import Blueprint, jsonify
from app.database import conn

admin_vendor_all_notice_list_service = Blueprint("admin_vendor_all_notice_list_service", __name__)

#----------------------------------  Topics : Admin view all vendor notice services, Author: Md. Iquball Hossain, Date: 03-12-2023 -------------

def get_vendor_all_notices(current_admin):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view user profiles.',
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.vendor_notice ORDER BY notice_time DESC")
        notices = cursor.fetchall()
        cursor.close()
        conn.putconn(connection)
        formatted_notices = []
        for notice in notices:
            notice_id = notice[0]
            vendor_id = notice[1]
            notice_title = notice[2]
            notice_topics = notice[3]
            notice_file = notice[4]
            notice_time = notice[5]
            date = notice_time.strftime("%Y-%m-%d")
            time = notice_time.strftime("%I:%M %p")
            formatted_notices.append({
                'notice_id': notice_id,
                'vendor_id': vendor_id,
                'notice_title': notice_title,
                'notice_topics': notice_topics,
                'notice_file': notice_file,
                'notice_date': date,
                'notice_time': time,
            })
        total_notices = len(notices)
        return jsonify({
            'success': True,
            'message': 'All Notices view successful',
            'total_notices': total_notices,
            'data': formatted_notices
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500


#----------------------------------  Topics : Admin view single vendor notice services, Author: Md. Iquball Hossain, Date: 03-12-2023 -------------

def get_vendor_single_notices(current_admin,vendor_id):
    try:
        if not current_admin or current_admin.get('admin_role', '').lower() != 'super admin':
            return jsonify({
                'success': False,
                'message': 'Permission denied. Only Super Admin can view user profiles.',
            }), 403
        connection = conn.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin.vendor_notice WHERE vendor_id = %s ORDER BY notice_time DESC", (vendor_id,))
        notices = cursor.fetchall()
        cursor.close()
        connection.close()
        formatted_notices = []
        for notice in notices:
            notice_id = notice[0]
            vendor_id = notice[1]
            notice_title = notice[2]
            notice_topics = notice[3]
            notice_file = notice[4]
            notice_time = notice[5]
            date = notice_time.strftime("%Y-%m-%d")
            time = notice_time.strftime("%I:%M %p")
            formatted_notices.append({
                'notice_id': notice_id,
                'vendor_id': vendor_id,
                'notice_title': notice_title,
                'notice_topics': notice_topics,
                'notice_file': notice_file,
                'notice_date': date,
                'notice_time': time,
            })
        total_notices = len(notices)
        return jsonify({
            'success': True,
            'message': f'All notices for vendor ID {vendor_id} viewed successfully',
            'total_notices': total_notices,
            'data': formatted_notices
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred: ' + str(e)}), 500

