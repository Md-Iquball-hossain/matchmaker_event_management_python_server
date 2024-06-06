from flask import Blueprint
from app.user.services.user_service import user_get_vendors_by_business_category, user_get_vendors_by_id, create_user_service_form
from utils.decorator.auth_checker import user_token_authentication

user_service_routes = Blueprint("user_service_routes", __name__)

#----------- Topics : user view vendor profile list using business category, Author: Md. Iquball Hossain, Date: 24-12-2023 ---------------

@user_service_routes.route("/user_view_vendors_list_by_category/<string:business_category>", methods=["GET"])
@user_token_authentication()
def user_view_vendors_by_category(current_user, business_category):
    return user_get_vendors_by_business_category(current_user, business_category)

#----------- Topics : user view vendor single profile from using vendor_id, Author: Md. Iquball Hossain, Date: 24-12-2023 ---------------

@user_service_routes.route("/user_view_vendors_single_service_by_id/<int:vendor_id>", methods=["GET"])
@user_token_authentication()
def user_view_vendors_service_by_id(current_user, vendor_id):
    return user_get_vendors_by_id(current_user, vendor_id)

#----------- Topics : create service from using vendor_id, Author: Md. Iquball Hossain, Date: 24-12-2023 ---------------

@user_service_routes.route("/create_user_service_form/<int:vendor_id>", methods=["POST"])
@user_token_authentication()
def user_service_form_create(current_user, vendor_id):
    return create_user_service_form(current_user, vendor_id)