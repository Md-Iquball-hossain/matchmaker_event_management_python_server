
from flask import Blueprint
from app.vendor.services.vendor_helpdesk_service import create_helpdesk_message, get_vendor_helpdesk_messages, update_helpdesk_message
from utils.decorator.auth_checker import vendor_token_authentication

vendor_helpdesk_message = Blueprint("vendor_helpdesk_message", __name__)

#----------------------------------  Topics : vendor create helpdesk message Endpoint, Author: Md. Iquball Hossain, Date: 04-11-2023 ------------------------

@vendor_helpdesk_message.route("/create_helpdesk_message", methods=["POST"])
@vendor_token_authentication()
def vendor_create_helpdesk_message(current_vendor):
    return create_helpdesk_message(current_vendor)

#----------------------------------  Topics : vendor view helpdesk message Endpoint, Author: Md. Iquball Hossain, Date: 04-11-2023 --------------------------

@vendor_helpdesk_message.route("/view_helpdesk_message", methods=["GET"])
@vendor_token_authentication()
def vendor_view_helpdesk_message(current_vendor):
    return get_vendor_helpdesk_messages(current_vendor)

#----------------------------------  Topics : vendor edit helpdesk message Endpoint, Author: Md. Iquball Hossain, Date: 05-11-2023 ----------------------------

@vendor_helpdesk_message.route("/edit_helpdesk_message/<int:helpdesk_id>", methods=["PUT"])
@vendor_token_authentication()
def vendor_edit_helpdesk_message(helpdesk_id):
    return update_helpdesk_message(helpdesk_id)