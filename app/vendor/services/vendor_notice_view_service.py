
#----------------------------------  Topics : view vendor notice form admin API service, Author: Md. Iquball Hossain, Date: 28-11-2023 -------------------------------------

from flask import Blueprint, jsonify
import psycopg2
from app.database import conn

vendor_notice_view_service = Blueprint('vendor_notice_view_service', __name__)

def vendor_notice_from_admin(current_vendor):
    try:
        connection = conn.getconn()
        cursor = connection.cursor()
        vendor_id = current_vendor.get('id')
        business_category = current_vendor.get('business_category')
        if not vendor_id and not business_category:
            return jsonify({
                'success': False,
                'message': 'Vendor ID or business category is missing.'
            }), 400
        if vendor_id:
            query = "SELECT * FROM vendors.vendor WHERE id = %s"
            cursor.execute(query, (vendor_id,))
        else:
            query = "SELECT * FROM vendors.vendor WHERE business_category = %s::vendors.business_type"
            cursor.execute(query, (business_category,))
        vendor_data = cursor.fetchone()
        if not vendor_data:
            return jsonify({
                'success': False,
                'message': 'Vendor profile not found.'
            }), 404
        cursor.execute("SELECT * FROM dbo.notice WHERE vendor_id = %s", (vendor_id,))
        notices = cursor.fetchall()
        notice_list = []
        for notice in notices:
            notice_dict = {
                'id': notice[0],
                'notice_title': notice[1],
                'notice_topics': notice[2],
                'notice_file': notice[3],
            }
            notice_list.append(notice_dict)
        cursor.close()
        return jsonify({
            'success': True,
            'message': 'Notices for the vendor retrieved successfully',
            'data': notice_list
        }), 200
    except psycopg2.Error as e:
        print(e)
        return jsonify({
            'success': False,
            'message': 'Failed to fetch notices for the vendor.'
        }), 500
    finally:
        conn.putconn(connection)

#----------------------------------  Topics : view vendor notice form admin as recent month and specific year API service, Author: Md. Iquball Hossain, Date: 30-11-2023 -------------------------------------

def vendor_special_notice_from_admin(current_vendor):
    try:
        if current_vendor is None or 'id' not in current_vendor:
            return False, {'success': False}
        connection = conn.getconn()
        cursor = connection.cursor()
        vendor_id = current_vendor.get('id')
        cursor.execute("SELECT id, notice_title, notice_topics, notice_file, notice_time FROM admin.vendor_notice WHERE vendor_id = %s ORDER BY notice_time DESC", (vendor_id,))
        notices = cursor.fetchall()
        recent_month_notices = {}
        same_year_notices = {}
        for notice in notices:
            notice_id, notice_title, notice_topics, notice_file, notice_time = notice
            notice_date_formatted = notice_time.strftime('%Y-%m-%d')
            notice_time_formatted = notice_time.strftime('%I:%M %p')
            notice_data = {
                'notice_id': notice_id,
                'vendor_id': vendor_id,
                'notice_title': notice_title,
                'notice_topics': notice_topics,
                'notice_file': notice_file,
                'notice_date': notice_date_formatted,
                'notice_time': notice_time_formatted
            }
            year_month = notice_time.strftime("%Y-%m")
            if year_month not in recent_month_notices:
                recent_month_notices[year_month] = []
            recent_month_notices[year_month].append(notice_data)
            same_year = notice_time.strftime("%Y")
            if same_year not in same_year_notices:
                same_year_notices[same_year] = []
            same_year_notices[same_year].append(notice_data)
        return {
            'success': True,
            'recent_month_notices': recent_month_notices,
            'same_year_notices': same_year_notices
        }
    except psycopg2.Error as e:
        return {'error': str(e)}
    finally:
        connection.close()
        conn.putconn(connection)
        cursor.close()