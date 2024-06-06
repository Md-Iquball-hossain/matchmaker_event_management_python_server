
from flask import Blueprint, jsonify, request
from app.admin.vendor_admin.services.admin_view_vendor_helpdesk_msg import get_helpdesk_messages,edit_helpdesk_status
from utils.decorator.auth_checker import admin_token_authentication

admin_vendor_helpdesk_message_routes = Blueprint("admin_vendor_helpdesk_message_routes", __name__)

#----------------------------------  Topics : Admin view vendor's helpdesk message routes list routes, Author: Md. Iquball Hossain, Date: 03-12-2023 --------------------------------

@admin_vendor_helpdesk_message_routes.route("/admin_view_vendors_all_message", methods=["GET"])
@admin_token_authentication()
def admin_view_vendors_all_message(current_admin):
    return get_helpdesk_messages(current_admin)

from flask import request
@admin_vendor_helpdesk_message_routes.route("/admin_edit_vendors_helpdesk_status/<int:helpdesk_id>", methods=["PUT"])
@admin_token_authentication()
def admin_edit_vendors_helpdesk_message(current_admin, helpdesk_id):
    new_status = request.form.get('new_status')
    if not new_status:
        return jsonify({
            'success': False,
            'message': 'No new_status provided in the form data.'
        }), 400
    return edit_helpdesk_status(current_admin, helpdesk_id, new_status)
