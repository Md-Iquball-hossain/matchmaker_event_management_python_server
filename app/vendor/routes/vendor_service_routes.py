
from flask import Blueprint
from app.vendor.services.vendor_service import create_vendor_service, get_vendor_service, edit_vendor_service, get_user_service,change_user_message_status
from utils.decorator.auth_checker import vendor_token_authentication

vendor_service_routes = Blueprint("vendor_service_routes", __name__)

#----------------------------------  Topics : vendor create service form Endpoint, Author: Md. Iquball Hossain, Date: 17-12-2023 ------------------------

@vendor_service_routes.route("/create_vendor_service", methods=["POST"])
@vendor_token_authentication()
def vendor_create_service_form(current_vendor):
    return create_vendor_service(current_vendor)

#----------------------------------  Topics : view vendor service form Endpoint, Author: Md. Iquball Hossain, Date: 18-12-2023 ------------------------

@vendor_service_routes.route("/view_vendor_service", methods=["GET"])
@vendor_token_authentication()
def view_vendor_service_form(current_vendor):
    return get_vendor_service(current_vendor)

#----------------------------------  Topics : edit vendor service form Endpoint, Author: Md. Iquball Hossain, Date: 18-12-2023 ------------------------

@vendor_service_routes.route("/edit_vendor_service", methods=["PUT"])
@vendor_token_authentication()
def update_vendor_service_form(current_vendor):
    return edit_vendor_service(current_vendor)

#----------------------------------  Topics : view user service form vendor dashboard, Author: Md. Iquball Hossain, Date: 18-12-2023 ------------------------

@vendor_service_routes.route("/view_user_message_by_vendor", methods=["GET"])
@vendor_token_authentication()
def get_user_message_by_vendor(current_vendor):
    return get_user_service(current_vendor)

#----------------------------------  Topics : edit user service form vendor dashboard, Author: Md. Iquball Hossain, Date: 18-12-2023 ------------------------

@vendor_service_routes.route("/edit_user_message_status_by_vendor/<int:user_service_id>", methods=["PUT"])
@vendor_token_authentication()
def edit_user_message_by_vendor(current_vendor,user_service_id):
    return change_user_message_status(current_vendor,user_service_id)